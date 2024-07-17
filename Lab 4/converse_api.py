import boto3, json, os
from opentelemetry import propagate, trace, metrics

# Import necessary libraries for OpenTelemetry exporters, metrics, SDK, instrumentation, and propagators
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter # Export trace data via gRPC
from opentelemetry.metrics import CallbackOptions, Observation  # Handle metric observations
from opentelemetry.sdk.trace import TracerProvider  # Manages the tracing setup
from opentelemetry.sdk.trace.export import BatchSpanProcessor  # Batches spans before exporting
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator  # Generates trace IDs in X-Ray format
from opentelemetry.sdk.resources import SERVICE_NAME, Resource  # Provides information about the service
from opentelemetry.sdk.metrics import MeterProvider  # Manages metrics setup
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader # Export metrics periodically
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter # Export metrics via gRPC
from opentelemetry.propagators.aws import AwsXRayPropagator  # Propagate trace context in X-Ray format
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor  # Auto-instrument Botocore calls
from opentelemetry.instrumentation.requests import RequestsInstrumentor  # Auto-instrument Requests calls

# Get global instances of the tracer and meter for OpenTelemetry
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# --- Instrumentation Setup ---
def setup_instrumentation():
    BotocoreInstrumentor().instrument() # Enable automatic tracing for AWS SDK calls
    RequestsInstrumentor().instrument() # Enable automatic tracing for external HTTP requests

# --- OpenTelemetry Setup ---
def setup_opentelemetry(tracer, meter):
    # Set AWS X-Ray as the global propagator for context propagation
    propagate.set_global_textmap(AwsXRayPropagator())
    
    # Define resource attributes for the service (or load from env variable)
    resource_attributes = { 'service.name': 'bedrock-workshop-app' }
    if (os.environ.get("OTEL_RESOURCE_ATTRIBUTES")):
        resource_attributes = None
    resource = Resource.create(attributes=resource_attributes)

    # --- Traces ---
    # Set up batch processing and OTLP export for traces
    processor = BatchSpanProcessor(OTLPSpanExporter())
    tracer_provider = TracerProvider(
        resource=resource, 
        active_span_processor=processor,
        id_generator=AwsXRayIdGenerator()) # Use X-Ray compatible IDs
    
    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer(__name__)

    # --- Metrics ---
    # Set up periodic export of metrics using OTLP
    metric_reader = PeriodicExportingMetricReader(exporter=OTLPMetricExporter(), export_interval_millis=1000)
    metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    
    metrics.set_meter_provider(metric_provider)
    meter = metrics.get_meter(__name__)

# Initialize Bedrock client
session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

# --- Metrics Definitions ---
# Define common attributes for all metrics
common_attributes = { 'signal': 'metric', 'language': 'python-312', 'metricType': 'request' }

# Create metric counters for tokens and latency
total_tokens_sent = meter.create_counter("total_tokens_sent", description="Total tokens sent to Bedrock")
total_tokens_received = meter.create_counter("total_tokens_received", description="Total tokens received from Bedrock")
total_tokens = meter.create_counter("total_tokens", description="Total tokens (sent + received)")
latency = meter.create_counter("bedrock_latency", description="Bedrock latency", unit='ms')

# Initialize instrumentation and OpenTelemetry
setup_instrumentation()
setup_opentelemetry(tracer, meter)

message_list = []

while True:
    # Get user input and check for exit condition
    inp = input("User: ")
    if inp == "exit":
        break

    # Construct the message to send to Bedrock
    initial_message = {
        "role": "user",
        "content": [
            { "text": inp } 
        ],
    }
    message_list.append(initial_message) 

    # --- Traced Span for Bedrock Call ---
    with tracer.start_as_current_span("outgoing-request-call") as span:
        # Set span attributes for context
        span.set_attribute("language", "python-auto-instrumentation")
        span.set_attribute("signal", "trace")
        span.add_event("Making a request to Bedrock") # Add an event to the span

        # Call the Bedrock Converse API
        response = bedrock.converse(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            messages=message_list,
            inferenceConfig={
                "maxTokens": 2000,
                "temperature": 0.5
            },
        )

        # Record metrics after the Bedrock call
        total_tokens_sent.add(response['usage']['inputTokens'], attributes=common_attributes)
        total_tokens_received.add(response['usage']['outputTokens'], attributes=common_attributes)
        total_tokens.add(response['usage']['totalTokens'], attributes=common_attributes)
        latency.add(response['metrics']['latencyMs'], attributes=common_attributes)

        # Append the received message to the conversation history
        message_list.append(response['output']['message'])

    # Extract and print the system's response message
    response_message = response['output']['message']['content'][0]['text']
    print("System:", response_message) 
