import boto3, json, os
from opentelemetry import propagate, trace, metrics

# Exporter Libraries
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Metrics Library
from opentelemetry.metrics import CallbackOptions, Observation

# SDK Libraries
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Propogators Library
from opentelemetry.propagators.aws import AwsXRayPropagator
from opentelemetry.propagators.aws.aws_xray_propagator import (
    TRACE_ID_DELIMITER,
    TRACE_ID_FIRST_PART_LENGTH,
    TRACE_ID_VERSION,
)

# Instrumentation Libraries
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Setting up Instrumentation
def setup_instrumentation():
    BotocoreInstrumentor().instrument()
    RequestsInstrumentor().instrument()

# Setting up opentelemetry
def setup_opentelemetry(tracer, meter):
    # Set up AWS X-Ray Propagator
    propagate.set_global_textmap(AwsXRayPropagator())
    # Service name is required for most backends
    resource_attributes = { 'service.name': 'bedrock-workshop-app' }
    if (os.environ.get("OTEL_RESOURCE_ATTRIBUTES")):
        resource_attributes = None
    resource = Resource.create(attributes=resource_attributes)

    # Setting up Traces
    processor = BatchSpanProcessor(OTLPSpanExporter())
    tracer_provider = TracerProvider(
        resource=resource, 
        active_span_processor=processor,
        id_generator=AwsXRayIdGenerator())

    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer(__name__)

    # Setting up Metrics
    metric_reader = PeriodicExportingMetricReader(exporter=OTLPMetricExporter(), export_interval_millis=1000)
    metric_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

    metrics.set_meter_provider(metric_provider)
    meter = metrics.get_meter(__name__)

session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')


common_attributes = { 'signal': 'metric', 'language': 'python-312', 'metricType': 'request' }

# register total bytes sent counter
total_tokens_sent=meter.create_counter(
    name="total_tokens_sent",
    description="Keeps a sum of the total amount of tokens sent to Bedrock"
)

total_tokens_received=meter.create_counter(
    name="total_tokens_received",
    description="Keeps a sum of the total amount of tokens received from Bedrock."
)

total_tokens=meter.create_counter(
    name="total_tokens",
    description="Keeps a sum of the total amount of tokens sent and received while suing the Bedrock service."
)

latency=meter.create_counter(
    name="bedrock_latency",
    description="Keeps a sum of the total amount of latency.",
    unit='ms'
)

setup_instrumentation()
setup_opentelemetry(tracer, meter)

message_list = []

while True:
    inp = input("User: ")

    if inp == "exit":
        break

    initial_message = {
        "role": "user",
        "content": [
            { "text": inp } 
        ],
    }

    message_list.append(initial_message)

    with tracer.start_as_current_span("outgoing-request-call") as span:

        # Demonstrates setting an attribute, a k/v pairing.
        span.set_attribute("language", "python-auto-instrumentation")
        span.set_attribute("signal", "trace")

        # Demonstrating adding events to the span. Think of events as a primitive log.
        span.add_event("Making a request to Bedrock")


        response = bedrock.converse(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            messages=message_list,
            inferenceConfig={
                "maxTokens": 2000,
                "temperature": 0.5
            },
        )

        total_tokens_sent.add(response['usage']['inputTokens'], attributes=common_attributes)
        total_tokens_received.add(response['usage']['outputTokens'], attributes=common_attributes)
        total_tokens.add(response['usage']['totalTokens'], attributes=common_attributes)
        latency.add(response['metrics']['latencyMs'], attributes=common_attributes)

        message_list.append(response['output']['message'])

    response_message = response['output']['message']['content'][0]['text']
    # print(json.dumps(response_message, indent=4))
    print(response_message)

    # print(json.dumps(message_list, indent=4))

