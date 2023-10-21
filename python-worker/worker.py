import asyncio

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor
from temporalio.worker import Worker

from greeting import GreetingWorkflow, compose_greeting


def init_tracer():
    # Setup global tracer for workflow traces
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "my-service"}))
    exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)


async def main():
    init_tracer()

    # Connect client
    client = await Client.connect(
        "localhost:7233",
        # Use OpenTelemetry interceptor
        interceptors=[TracingInterceptor()],
    )

    # Run the worker
    worker = Worker(
        client,
        task_queue="open_telemetry-task-queue",
        workflows=[GreetingWorkflow],
        activities=[compose_greeting],
	)
    print("Starting worker...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
