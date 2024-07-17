# OpenTelemetry Instrumentation for Bedrock Chatbot

This project demonstrates how to instrument a Python-based chat interface with Amazon Bedrock using OpenTelemetry. It enables you to gain insights into the performance, usage patterns, and behavior of your chatbot interactions.

## Overview

This script combines:

- **Amazon Bedrock:**  For engaging conversational AI capabilities.
- **OpenTelemetry:** For observability, providing detailed traces and metrics about the chatbot's interactions with Bedrock.
- **Botocore & Requests Instrumentation:** Automatically instruments calls to AWS services (Botocore) and external HTTP requests (Requests).

## Key Features

- **Tracing:**  Captures detailed information about each interaction, including latency, request/response payloads (if configured), and errors.
- **Metrics:**  Collects key metrics like:
    - `total_tokens_sent`
    - `total_tokens_received`
    - `total_tokens` (total sent and received)
    - `bedrock_latency`
- **AWS X-Ray Compatibility:**  Propagates trace context using the AWS X-Ray format, allowing seamless integration with X-Ray for distributed tracing.
- **OTLP Export:**  Exports traces and metrics in the OpenTelemetry Protocol (OTLP) format to a compatible backend (e.g., AWS Managed Service for Prometheus, Jaeger, or other OTLP-compliant systems). 

## Setup

1. **Prerequisites:**
   - Python 3.12+
   - `boto3`
   - `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-instrumentation-botocore`, `opentelemetry-instrumentation-requests`, `opentelemetry-exporter-otlp-proto-grpc` (Install using `pip install ...`)
   - OpenTelemetry Collector or a compatible backend (optional, but recommended for visualization and analysis)
   - An AWS account with Bedrock configured

2. **Configuration (Optional):**
   - Set the `OTEL_RESOURCE_ATTRIBUTES` environment variable to customize resource attributes for your service.
   - Configure the `OTLPSpanExporter` and `OTLPMetricExporter` to point to your desired backend.

## Usage

1. Run the script.
2. Start chatting with the Bedrock-powered chatbot.
3. Observe the collected traces and metrics in your OpenTelemetry backend.

## How It Works

1. **Setup:**
   - Sets up OpenTelemetry instrumentation for Botocore and Requests libraries.
   - Configures the AWS X-Ray Propagator.
   - Initializes the OpenTelemetry Tracer Provider and Meter Provider.
   - Registers the metric counters.
2. **Main Loop:**
   - Prompts the user for input.
   - Constructs a message for Bedrock.
   - Makes a call to `bedrock.converse` within a traced span, recording relevant attributes and events.
   - Extracts metrics from the response.
   - Prints the Bedrock response.

## Customization

- Explore different Bedrock models.
- Adjust the conversation parameters (e.g., `temperature`).
- Extend the instrumentation to other parts of your application (e.g., database calls, background tasks).
- Add custom attributes and events to your spans to capture more context.

Let me know if you'd like assistance with configuration, deployment, or any other aspects of this instrumentation setup!