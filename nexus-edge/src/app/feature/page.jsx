"use client";
import React, { useState } from 'react';
import {
  Plug, Wifi, Database, Eye, Shield, Cloud,
  FileText, Zap, Server, Cpu, BarChart3,
  Settings, ArrowRight, CheckCircle, XCircle, Check,
  AlertTriangle, Heart, Network, Users, FileDown,
  FileCode, TestTube, Tag, Clock, Copy, RefreshCw,
  Bell, Container, GitBranch, Gauge, Lock, BrickWallFire,
  Menu, X
} from 'lucide-react';
import { useRouter } from 'next/navigation';

const App = () => {
  const [activeSection, setActiveSection] = useState('overview');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const router = useRouter();

  const productPrice = () => {
    router.push('/product/pricing');
  };

  const sections = [
    { id: 'overview', name: 'Overview', icon: <Settings className="w-5 h-5" /> },
    { id: 'device', name: 'Device Protocol', icon: <Plug className="w-7 h-5" /> },
    { id: 'data', name: 'Data Management', icon: <Database className="w-5 h-5" /> },
    { id: 'visualization', name: 'Visualization', icon: <BarChart3 className="w-5 h-5" /> },
    { id: 'security', name: 'Security', icon: <Shield className="w-5 h-5" /> },
    { id: 'integration', name: 'Integration', icon: <Cloud className="w-5 h-5" /> },
    { id: 'productivity', name: 'Productivity', icon: <FileText className="w-5 h-5" /> },
    { id: 'advanced', name: 'Advanced', icon: <Zap className="w-5 h-5" /> }
  ];

  const FeatureCard = ({ icon, title, description, features = [], complete = true }) => (
    <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6 hover:border-purple-400/40 transition-all duration-300">
      <div className="flex items-start mb-4">
        <div className="p-3 rounded-xl bg-gradient-to-br from-purple-600 to-indigo-600 mr-4">
          {icon}
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
          <p className="text-purple-200">{description}</p>
        </div>
        <div className={complete ? "text-green-400" : "text-red-400"}>
          {complete ? <CheckCircle className="w-6 h-6" /> : <XCircle className="w-6 h-6" />}
        </div>
      </div>
      {features.length > 0 && (
        <ul className="space-y-2">
          {features.map((feature, index) => (
            <li key={index} className="flex items-center text-purple-100">
              <Check className="w-4 h-4 text-green-400 mr-3 flex-shrink-0" />
              <span className="text-sm">{feature}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );

  const OverviewSection = () => (
    <div className="space-y-8">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          NexusEdge IIoT Gateway
        </h1>
        <p className="text-xl text-purple-200 max-w-4xl mx-auto leading-relaxed">
          Industrial IoT Gateway Platform - Connecting Edge Devices to Cloud Services with Secure Protocols.
          Enterprise-grade solution for industrial automation and smart manufacturing.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6 text-center">
          <Plug className="w-12 h-12 text-purple-400 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-white mb-2">500+</h3>
          <p className="text-purple-200">Device Protocols</p>
        </div>
        <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6 text-center">
          <Shield className="w-12 h-12 text-purple-400 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-white mb-2">Military-Grade</h3>
          <p className="text-purple-200">Security Standards</p>
        </div>
        <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6 text-center">
          <Cloud className="w-12 h-12 text-purple-400 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-white mb-2">Multi-Cloud</h3>
          <p className="text-purple-200">Integration Ready</p>
        </div>
        <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6 text-center">
          <Zap className="w-12 h-12 text-purple-400 mx-auto mb-4" />
          <h3 className="text-2xl font-bold text-white mb-2">Edge Analytics</h3>
          <p className="text-purple-200">Real-time Processing</p>
        </div>
      </div>

      <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/30 to-indigo-900/30 border border-purple-500/20 rounded-2xl p-8">
        <h2 className="text-3xl font-bold text-white mb-6 text-center">Enterprise IIoT Solution</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Settings className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Device Management</h3>
            <p className="text-purple-200">Complete protocol support and device integration</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Shield className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Security First</h3>
            <p className="text-purple-200">End-to-end encryption and compliance</p>
          </div>
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-600 to-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Cloud className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">Cloud Integration</h3>
            <p className="text-purple-200">Seamless connection to major cloud platforms</p>
          </div>
        </div>
      </div>
    </div>
  );

  const DeviceProtocolSection = () => (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold text-white mb-4">Device & Protocol Management</h2>
        <p className="text-xl text-purple-200">Comprehensive device discovery and protocol handling</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <FeatureCard
          icon={<Wifi className="w-6 h-6 text-white" />}
          title="Auto Device Discovery"
          description="Automatically scan and discover devices in your network"
          features={[
            "Modbus scan for industrial devices",
            "BACnet discovery for building automation",
            "OPC UA browse for enterprise systems",
            "Automatic device identification and classification"
          ]}
        />

        <FeatureCard
          icon={<Plug className="w-6 h-6 text-white" />}
          title="Driver Library"
          description="Repository of ready-to-use drivers for common devices and protocols"
          features={[
            "Siemens S7 series PLC drivers",
            "Schneider Electric Modicon drivers",
            "ABB AC500 and 800xA drivers",
            "Rockwell Automation Allen-Bradley drivers",
            "Mitsubishi, Omron, and other vendor-specific drivers"
          ]}
        />

        <FeatureCard
          icon={<CheckCircle className="w-6 h-6 text-white" />}
          title="Connection Tester"
          description="Test protocol connections before deployment"
          features={[
            "Real-time connection testing",
            "Protocol-specific diagnostic tools",
            "Connection health monitoring",
            "Pre-deployment validation"
          ]}
        />

        <FeatureCard
          icon={<Database className="w-6 h-6 text-white" />}
          title="Tag Browser & Mapping"
          description="Browse data points and map to gateway data models"
          features={[
            "PLC/IED/IoT device tag browsing",
            "Hierarchical data structure visualization",
            "Drag-and-drop tag mapping",
            "Bulk tag import/export functionality"
          ]}
        />

        <FeatureCard
          icon={<ArrowRight className="w-6 h-6 text-white" />}
          title="Protocol Converter"
          description="Map between different protocols seamlessly"
          features={[
            "Modbus to MQTT conversion",
            "OPC UA to REST API mapping",
            "Multi-protocol data routing",
            "Real-time protocol translation"
          ]}
        />
      </div>
    </div>
  );

  const DataManagementSection = () => (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold text-white mb-4">Data Management & Processing</h2>
        <p className="text-xl text-purple-200">Advanced data handling and processing capabilities</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <FeatureCard
          icon={<Settings className="w-6 h-6 text-white" />}
          title="Data Transformation"
          description="Low-code functions for data normalization and processing"
          features={[
            "Data normalization and scaling",
            "Unit conversion utilities",
            "Filtering and aggregation functions",
            "Custom transformation rules"
          ]}
        />

        <FeatureCard
          icon={<Database className="w-6 h-6 text-white" />}
          title="Data Buffering & Store-and-Forward"
          description="Reliable data handling during network interruptions"
          features={[
            "Automatic data buffering during outages",
            "Store-and-forward mechanism",
            "Persistent storage for critical data",
            "Automatic recovery and data sync"
          ]}
        />

        <FeatureCard
          icon={<Server className="w-6 h-6 text-white" />}
          title="Time-Series Database Integration"
          description="Built-in and external database support"
          features={[
            "Built-in InfluxDB/TimescaleDB support",
            "External PostgreSQL integration",
            "MongoDB connectivity options",
            "Database performance optimization"
          ]}
        />

        <FeatureCard
          icon={<AlertTriangle className="w-6 h-6 text-white" />}
          title="Event & Alarm Management"
          description="Rule-based event detection and notification system"
          features={[
            "Threshold-based alarm conditions",
            "Custom event rules configuration",
            "Alarm prioritization and categorization",
            "Notification escalation procedures"
          ]}
        />

        <FeatureCard
          icon={<BarChart3 className="w-6 h-6 text-white" />}
          title="Edge Analytics"
          description="Lightweight analytics at the edge"
          features={[
            "Statistical analysis functions",
            "FFT for signal processing",
            "Lightweight anomaly detection",
            "Real-time data insights"
          ]}
        />
      </div>
    </div>
  );

  const VisualizationSection = () => (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold text-white mb-4">Visualization & Monitoring</h2>
        <p className="text-xl text-purple-200">Real-time dashboards and comprehensive monitoring</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <FeatureCard
          icon={<BarChart3 className="w-6 h-6 text-white" />}
          title="Real-Time Dashboard"
          description="Interactive drag-and-drop dashboard builder"
          features={[
            "Drag-and-drop widget system",
            "Chart, gauge, and table widgets",
            "Geospatial mapping capabilities",
            "Custom dashboard templates"
          ]}
        />

        <FeatureCard
          icon={<Wifi className="w-6 h-6 text-white" />}
          title="Protocol Traffic Monitor"
          description="Monitor protocol traffic in real-time"
          features={[
            "Per-protocol packet monitoring",
            "Traffic analysis and statistics",
            "Protocol-specific diagnostic views",
            "Bandwidth utilization tracking"
          ]}
        />

        <FeatureCard
          icon={<Heart className="w-6 h-6 text-white" />}
          title="Health Monitoring"
          description="Comprehensive system health monitoring"
          features={[
            "Device connection status tracking",
            "Network latency monitoring",
            "Packet loss detection",
            "Gateway uptime statistics"
          ]}
        />

        <FeatureCard
          icon={<Bell className="w-6 h-6 text-white" />}
          title="Alerting System"
          description="Multi-channel notification system"
          features={[
            "Email notification integration",
            "Telegram bot alerts",
            "Slack webhook support",
            "Microsoft Teams integration"
          ]}
        />

        <FeatureCard
          icon={<Network className="w-6 h-6 text-white" />}
          title="Network Topology View"
          description="Visual representation of device network"
          features={[
            "Graph-based network visualization",
            "Device relationship mapping",
            "Connection path analysis",
            "Network performance metrics"
          ]}
        />
      </div>
    </div>
  );

  const SecuritySection = () => (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold text-white mb-4">Security & Compliance</h2>
        <p className="text-xl text-purple-200">Enterprise-grade security and compliance features</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <FeatureCard
          icon={<Shield className="w-6 h-6 text-white" />}
          title="TLS/SSL & Certificate Management"
          description="Comprehensive certificate management system"
          features={[
            "X.509 certificate management",
            "OPC UA security certificate handling",
            "MQTT TLS configuration",
            "HTTPS certificate automation"
          ]}
        />

        <FeatureCard
          icon={<Users className="w-6 h-6 text-white" />}
          title="Role-Based Access for Protocols"
          description="Granular access control for protocol data"
          features={[
            "Protocol-specific access permissions",
            "User role management",
            "Access logging and auditing",
            "Multi-factor authentication support"
          ]}
        />

        <FeatureCard
          icon={<FileText className="w-6 h-6 text-white" />}
          title="Secure Audit Trail"
          description="Comprehensive configuration change logging"
          features={[
            "Detailed configuration change logs",
            "Audit trail export capabilities",
            "Compliance reporting tools",
            "Tamper-evident logging"
          ]}
        />

        <FeatureCard
          icon={<Lock className="w-6 h-6 text-white" />}
          title="Protocol Security Support"
          description="Industry-standard security protocol support"
          features={[
            "DNP3 Secure Authentication",
            "IEC 62351 for IEC61850/IEC104",
            "Modbus/TCP security extensions",
            "OPC UA advanced security features"
          ]}
        />

        <FeatureCard
          icon={<RefreshCw className="w-6 h-6 text-white" />}
          title="Firmware/Software Update Management"
          description="Secure and managed software updates"
          features={[
            "Centralized update management",
            "Secure firmware distribution",
            "Rollback capabilities",
            "Update scheduling and automation"
          ]}
        />
      </div>
    </div>
  );

  const IntegrationSection = () => (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold text-white mb-4">Integration & Scalability</h2>
        <p className="text-xl text-purple-200">Seamless integration with cloud platforms and devices</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <FeatureCard
          icon={<Cloud className="w-6 h-6 text-white" />}
          title="Northbound Integration"
          description="Cloud and historian platform integration"
          features={[
            "AWS IoT Core connectivity",
            "Azure IoT Hub integration",
            "Google Cloud IoT support",
            "OSIsoft PI System integration",
            "Ignition SCADA connectivity",
            "Kepware and Canary historian support"
          ]}
        />

        <FeatureCard
          icon={<Plug className="w-6 h-6 text-white" />}
          title="Southbound Device Integration"
          description="Vendor-specific device driver support"
          features={[
            "Siemens S7 PLC drivers",
            "Schneider M580 integration",
            "Allen-Bradley device support",
            "Mitsubishi and Omron drivers",
            "Generic protocol adapters"
          ]}
        />

        <FeatureCard
          icon={<Container className="w-6 h-6 text-white" />}
          title="Container/Edge App Deployment"
          description="Run external applications on the gateway"
          features={[
            "Docker container support",
            "K3s Kubernetes integration",
            "Resource allocation management",
            "Application lifecycle management"
          ]}
        />

        <FeatureCard
          icon={<BrickWallFire className="w-6 h-6 text-white" />}
          title="API Management"
          description="Expose APIs for external applications"
          features={[
            "REST API gateway functionality",
            "gRPC service exposure",
            "API rate limiting and throttling",
            "Authentication and authorization"
          ]}
        />

        <FeatureCard
          icon={<Server className="w-6 h-6 text-white" />}
          title="Multi-Gateway Management"
          description="Centralized management of multiple gateways"
          features={[
            "Single dashboard for all gateways",
            "Centralized configuration management",
            "Cross-gateway data aggregation",
            "Fleet-wide monitoring and alerts"
          ]}
        />
      </div>
    </div>
  );

  const ProductivitySection = () => (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold text-white mb-4">User Productivity Features</h2>
        <p className="text-xl text-purple-200">Non-login features for enhanced productivity</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <FeatureCard
          icon={<FileDown className="w-6 h-6 text-white" />}
          title="Configuration Export/Import"
          description="Backup and restore gateway configurations"
          features={[
            "JSON/YAML configuration export",
            "Bulk configuration import",
            "Version control integration",
            "Configuration comparison tools"
          ]}
        />

        <FeatureCard
          icon={<Copy className="w-6 h-6 text-white" />}
          title="Template & Profile"
          description="Reusable configuration templates"
          features={[
            "Protocol configuration templates",
            "Device profile management",
            "Template versioning",
            "Bulk template application"
          ]}
        />

        <FeatureCard
          icon={<Clock className="w-6 h-6 text-white" />}
          title="Scheduler"
          description="Scheduled data transmission and processing"
          features={[
            "Time-based data sending rules",
            "Daily batch processing",
            "Cron-style scheduling",
            "Event-triggered scheduling"
          ]}
        />

        <FeatureCard
          icon={<TestTube className="w-6 h-6 text-white" />}
          title="Simulation Mode"
          description="Virtual device testing environment"
          features={[
            "Dummy Modbus server simulation",
            "Virtual OPC UA server",
            "Protocol testing sandbox",
            "Load testing capabilities"
          ]}
        />

        <FeatureCard
          icon={<Tag className="w-6 h-6 text-white" />}
          title="Tag Metadata Management"
          description="Enhanced tag information management"
          features={[
            "Tag description management",
            "Category and grouping",
            "Unit and scaling definitions",
            "Metadata bulk editing"
          ]}
        />
      </div>
    </div>
  );

  const AdvancedSection = () => (
    <div className="space-y-8">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-bold text-white mb-4">Advanced Enterprise Features</h2>
        <p className="text-xl text-purple-200">Cutting-edge capabilities for enterprise deployments</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <FeatureCard
          icon={<Zap className="w-6 h-6 text-white" />}
          title="High Availability & Failover"
          description="Enterprise-grade redundancy and failover"
          features={[
            "Gateway clustering support",
            "Automatic node failover",
            "Load balancing capabilities",
            "Zero-downtime deployment"
          ]}
        />

        <FeatureCard
          icon={<Cpu className="w-6 h-6 text-white" />}
          title="Edge ML/AI Integration"
          description="Machine learning at the edge"
          features={[
            "TensorFlow Lite model deployment",
            "ONNX model support",
            "Anomaly detection algorithms",
            "Real-time ML inference"
          ]}
        />

        <FeatureCard
          icon={<GitBranch className="w-6 h-6 text-white" />}
          title="Data Governance"
          description="Comprehensive data lineage and governance"
          features={[
            "Data lineage tracking",
            "Change audit trails",
            "Data quality metrics",
            "Governance policy enforcement"
          ]}
        />

        <FeatureCard
          icon={<FileCode className="w-6 h-6 text-white" />}
          title="Policy & Rule Engine"
          description="Advanced rule-based automation"
          features={[
            "Declarative rule configuration",
            "Conditional action triggers",
            "Complex business logic",
            "Rule version management"
          ]}
        />

        <FeatureCard
          icon={<Gauge className="w-6 h-6 text-white" />}
          title="Energy & OEE Dashboard"
          description="Industrial KPI monitoring and analysis"
          features={[
            "Overall Equipment Effectiveness tracking",
            "Energy consumption monitoring",
            "Production efficiency metrics",
            "Custom KPI dashboard builder"
          ]}
        />
      </div>
    </div>
  );

  const renderSection = () => {
    switch (activeSection) {
      case 'overview': return <OverviewSection />;
      case 'device': return <DeviceProtocolSection />;
      case 'data': return <DataManagementSection />;
      case 'visualization': return <VisualizationSection />;
      case 'security': return <SecuritySection />;
      case 'integration': return <IntegrationSection />;
      case 'productivity': return <ProductivitySection />;
      case 'advanced': return <AdvancedSection />;
      default: return <OverviewSection />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="backdrop-blur-xl bg-purple-900/30 border-b border-purple-500/20 sticky top-0 z-50">
        <div className="container mx-auto px-4 sm:px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center">
                  <Cpu className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-white">NexusEdge</span>
              </div>

              <div className="hidden lg:flex space-x-2 ml-8">
                {sections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-300 text-sm whitespace-nowrap ${activeSection === section.id
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                      : 'text-purple-200 hover:text-white hover:bg-purple-800/50'
                      }`}
                  >
                    {section.icon}
                    <span>{section.name}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={productPrice}
                className="hidden md:block text-sm bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-4 py-2 rounded-lg font-semibold transition-all transform hover:scale-105 whitespace-nowrap">
                Get Started
              </button>

              <button
                className="lg:hidden text-white p-2"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              >
                {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="lg:hidden backdrop-blur-xl bg-purple-900/30 border-t border-purple-500/20">
            <div className="container mx-auto px-4 py-3">
              <div className="flex flex-wrap gap-2">
                {sections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => {
                      setActiveSection(section.id);
                      setIsMobileMenuOpen(false);
                    }}
                    className={`flex items-center space-x-1 px-3 py-1.5 rounded-lg transition-all duration-300 text-sm whitespace-nowrap ${activeSection === section.id
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                      : 'text-purple-200 hover:text-white hover:bg-purple-800/50'
                      }`}
                  >
                    {section.icon}
                    <span>{section.name}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Mobile Menu */}
      <div className="lg:hidden backdrop-blur-xl bg-purple-900/30 border-b border-purple-500/20">
        <div className="container mx-auto px-6 py-3">
          <select
            value={activeSection}
            onChange={(e) => setActiveSection(e.target.value)}
            className="w-full bg-purple-800/50 border border-purple-500/30 rounded-lg px-4 py-2 text-white"
          >
            {sections.map((section) => (
              <option key={section.id} value={section.id} className="bg-purple-900">
                {section.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-12">
        {renderSection()}
      </main>

      {/* Footer */}
      <footer className="backdrop-blur-xl bg-purple-900/30 border-t border-purple-500/20 mt-20">
        <div className="container mx-auto px-6 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center">
                  <Cpu className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-white">NexusEdge</span>
              </div>
              <p className="text-purple-200">
                Industrial IoT Gateway Platform for secure, scalable industrial automation.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-white mb-4">Products</h3>
              <ul className="space-y-2 text-purple-200">
                <li><a href="#" className="hover:text-white transition-colors">Gateway Hardware</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Software Platform</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Cloud Services</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support Plans</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-white mb-4">Resources</h3>
              <ul className="space-y-2 text-purple-200">
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Reference</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Tutorials</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Community</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-white mb-4">Company</h3>
              <ul className="space-y-2 text-purple-200">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Partners</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-purple-500/20 mt-8 pt-8 text-center text-purple-300">
            <p>&copy; 2024 NexusEdge IIoT Gateway. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;