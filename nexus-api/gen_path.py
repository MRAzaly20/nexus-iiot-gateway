#!/usr/bin/env python3
# generate_project.py

import os

# Definisi struktur folder dan file kosong
project_structure = {
    "iiot_gateway_project": {
        "services": {
            "device_management": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "discovery.py": "",
                        "drivers.py": "",
                        "connections.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "discovery_engine.py": "",
                    "driver_loader.py": "",
                    "connection_tester.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "data_acquisition": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "tags.py": "",
                        "converter.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "tag_browser.py": "",
                    "mapper.py": "",
                    "protocol_converter.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "data_processing": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "transformation.py": "",
                        "buffering.py": "",
                        "storage.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "transformer.py": "",
                    "buffer_manager.py": "",
                    "db_integrator.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "event_alarm": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "rules.py": "",
                        "alarms.py": "",
                        "analytics.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "rule_engine.py": "",
                    "alarm_manager.py": "",
                    "analytics_engine.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "visualization_monitoring": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "dashboards.py": "",
                        "monitoring.py": "",
                        "topology.py": "",
                        "alerts.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "dashboard_renderer.py": "",
                    "monitor.py": "",
                    "topology_builder.py": "",
                    "alert_dispatcher.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "security": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "certificates.py": "",
                        "access.py": "",
                        "audit.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "cert_manager.py": "",
                    "access_controller.py": "",
                    "audit_logger.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "integration": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "cloud.py": "",
                        "historian.py": "",
                        "gateways.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "cloud_connector.py": "",
                    "historian_adapter.py": "",
                    "gateway_manager.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "user_productivity": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "config.py": "", # Gunakan config_api.py untuk menghindari konflik nama
                        "templates.py": "",
                        "scheduler.py": "",
                        "simulation.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "config_manager.py": "",
                    "template_engine.py": "",
                    "scheduler_engine.py": "",
                    "simulator.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "api_gateway": {
                "main.py": "",
                "api": {
                    "v1": {
                        "__init__.py": "",
                        "routes.py": ""
                    },
                    "__init__.py": ""
                },
                "core": {
                    "proxy.py": ""
                },
                "models.py": "",
                "config.py": "",
                "requirements.txt": ""
            },
            "shared": {
                "models": {
                    "__init__.py": "",
                    "common.py": "",
                    "messages.py": ""
                },
                "utils": {
                    "__init__.py": "",
                    "helpers.py": ""
                },
                "__init__.py": ""
            }
        },
        "infrastructure": {
            "message_broker": {
                "docker-compose.yml": "# Docker Compose untuk Message Broker (e.g., RabbitMQ, Kafka)"
            },
            "databases": {
                "docker-compose.yml": "# Docker Compose untuk Database (InfluxDB, TimescaleDB, PostgreSQL, MongoDB)"
            }
        },
        "docker-compose.yml": "# Orkestrasi utama untuk semua layanan microservices",
        "README.md": "# IIoT Gateway Project\n\nProyek Microservices IIoT Gateway menggunakan FastAPI.",
        "requirements-dev.txt": "# Dependensi untuk pengembangan (testing, linting)"
    }
}

def create_structure(base_path, structure):
    """Fungsi rekursif untuk membuat folder dan file."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    f.write(content)
            else:
                print(f"File already exists, skipping: {path}")

if __name__ == "__main__":
    current_dir = os.getcwd()
    project_name = list(project_structure.keys())[0] 
    project_path = os.path.join(current_dir, project_name)

    print(f"Generating project structure in: {project_path}")
    create_structure(current_dir, project_structure)
    print("Project structure generation complete!")
