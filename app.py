from flask import Flask, jsonify
import os

# OpenTelemetry Tracing
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# OpenTelemetry Metrics
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# OpenTelemetry Instrumentation
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# Common Resource
resource = Resource(attributes={
    "service.name": os.getenv("OTEL_SERVICE_NAME", "flask-app")
})

# 1. Tracing Setup
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)
span_exporter = OTLPSpanExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"), insecure=True)
tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))

# 2. Metrics Setup
metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"), insecure=True))
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)

# Instrument the Flask app
FlaskInstrumentor().instrument_app(app)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to your Python app!",
        "status": "Running",
        "environment": os.getenv("ENV", "development")
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # Using port 5000 as default for Flask, but can be configured
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
