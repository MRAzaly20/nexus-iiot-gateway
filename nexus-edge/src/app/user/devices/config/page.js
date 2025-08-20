"use client";
import React, { useState } from 'react';
import {
  Plug, Wifi, Search, Settings, Check, X,
  ArrowRight, Database, Map, RefreshCw,
  Play, Pause, Save, Upload, Download,
  ChevronDown, Filter, Plus, Edit, Trash2,
  Server, Cpu, HardDrive, Network, Eye,
  AlertCircle, Info, Zap, Shield
} from 'lucide-react';

const App = () => {
  const [activeTab, setActiveTab] = useState('discovery');
  const [isScanning, setIsScanning] = useState(false);
  const [devices, setDevices] = useState([
    { id: 1, name: 'Siemens S7-1200', ip: '192.168.1.100', type: 'PLC', status: 'connected', protocol: 'S7Comm' },
    { id: 2, name: 'Modbus Device A', ip: '192.168.1.101', type: 'Sensor', status: 'disconnected', protocol: 'Modbus RTU' },
    { id: 3, name: 'OPC UA Server', ip: '192.168.1.102', type: 'Server', status: 'connected', protocol: 'OPC UA' }
  ]);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [tagMappings, setTagMappings] = useState([
    { id: 1, source: 'Temperature_Sensor_1', target: 'Temp_Main_Tank', dataType: 'Float', unit: '°C' },
    { id: 2, source: 'Pressure_Gauge_1', target: 'Press_Main_Line', dataType: 'Integer', unit: 'PSI' }
  ]);
  const [protocolConversions, setProtocolConversions] = useState([
    { id: 1, source: 'Modbus RTU', target: 'MQTT', status: 'active', lastUsed: '2024-01-15 14:30' }
  ]);

  const tabs = [
    { id: 'discovery', name: 'Auto Discovery', icon: <Search className="w-4 h-4" /> },
    { id: 'library', name: 'Device Library', icon: <Database className="w-4 h-4" /> },
    { id: 'tester', name: 'Connection Tester', icon: <Settings className="w-4 h-4" /> },
    { id: 'browser', name: 'Tag Browser', icon: <Eye className="w-4 h-4" /> },
    { id: 'converter', name: 'Protocol Converter', icon: <ArrowRight className="w-4 h-4" /> }
  ];

  const protocols = [
    'Modbus TCP', 'Modbus RTU', 'OPC UA', 'MQTT', 'HTTP/HTTPS',
    'S7Comm', 'BACnet', 'IEC 60870-5-104', 'DNP3', 'Ethernet/IP'
  ];

  const deviceTypes = [
    'PLC', 'HMI', 'Sensor', 'Actuator', 'Gateway', 'Server', 'RTU', 'IED'
  ];

  // Auto Discovery Component
  const AutoDiscovery = () => (
    <div className="space-y-6">
      <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Auto Device Discovery</h2>
          <button
            onClick={() => setIsScanning(!isScanning)}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-all ${isScanning
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white'
              }`}
          >
            {isScanning ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            <span>{isScanning ? 'Stop Scan' : 'Start Scan'}</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-4">
            <label className="block text-purple-200 text-sm mb-2">Network Range</label>
            <input
              type="text"
              defaultValue="192.168.1.0/24"
              className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-4">
            <label className="block text-purple-200 text-sm mb-2">Scan Timeout (ms)</label>
            <input
              type="number"
              defaultValue="5000"
              className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
          </div>
          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-4">
            <label className="block text-purple-200 text-sm mb-2">Protocols</label>
            <select className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
              <option>All Protocols</option>
              <option>Modbus Only</option>
              <option>OPC UA Only</option>
            </select>
          </div>
        </div>

        {isScanning && (
          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-4 mb-6">
            <div className="flex items-center space-x-3">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-400"></div>
              <span className="text-purple-200">Scanning network... Found 3 devices</span>
            </div>
          </div>
        )}

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-purple-500/30">
                <th className="text-left py-3 px-4 text-purple-200 font-semibold">Device Name</th>
                <th className="text-left py-3 px-4 text-purple-200 font-semibold">IP Address</th>
                <th className="text-left py-3 px-4 text-purple-200 font-semibold">Type</th>
                <th className="text-left py-3 px-4 text-purple-200 font-semibold">Protocol</th>
                <th className="text-left py-3 px-4 text-purple-200 font-semibold">Status</th>
                <th className="text-left py-3 px-4 text-purple-200 font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody>
              {devices.map((device) => (
                <tr key={device.id} className="border-b border-purple-500/20 hover:bg-purple-800/20">
                  <td className="py-3 px-4 text-white">{device.name}</td>
                  <td className="py-3 px-4 text-purple-200">{device.ip}</td>
                  <td className="py-3 px-4 text-purple-200">{device.type}</td>
                  <td className="py-3 px-4 text-purple-200">{device.protocol}</td>
                  <td className="py-3 px-4">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${device.status === 'connected'
                        ? 'bg-green-900/50 text-green-400'
                        : 'bg-red-900/50 text-red-400'
                      }`}>
                      {device.status === 'connected' ? (
                        <Check className="w-3 h-3 mr-1" />
                      ) : (
                        <X className="w-3 h-3 mr-1" />
                      )}
                      {device.status}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <button
                      onClick={() => setSelectedDevice(device)}
                      className="text-purple-400 hover:text-purple-300 mr-3"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button className="text-red-400 hover:text-red-300">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  // Device Library Component
  const DeviceLibrary = () => (
    <div className="space-y-6">
      <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Device Library</h2>
          <button className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-4 py-2 rounded-lg font-semibold text-white transition-all">
            <Plus className="w-4 h-4" />
            <span>Add Device</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { name: 'Siemens S7 Series', type: 'PLC', protocol: 'S7Comm', vendor: 'Siemens', status: 'active' },
            { name: 'Modbus Generic', type: 'Generic', protocol: 'Modbus RTU/TCP', vendor: 'Universal', status: 'active' },
            { name: 'OPC UA Client', type: 'Client', protocol: 'OPC UA', vendor: 'Universal', status: 'active' },
            { name: 'Allen-Bradley', type: 'PLC', protocol: 'Ethernet/IP', vendor: 'Rockwell', status: 'active' },
            { name: 'Schneider M580', type: 'PLC', protocol: 'Modbus', vendor: 'Schneider', status: 'inactive' },
            { name: 'Mitsubishi FX', type: 'PLC', protocol: 'MC Protocol', vendor: 'Mitsubishi', status: 'active' }
          ].map((device, index) => (
            <div key={index} className="backdrop-blur-xl bg-purple-800/30 border border-purple-500/20 rounded-xl p-5 hover:border-purple-400/40 transition-all">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-white">{device.name}</h3>
                  <p className="text-purple-300 text-sm">{device.vendor}</p>
                </div>
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${device.status === 'active'
                    ? 'bg-green-900/50 text-green-400'
                    : 'bg-gray-900/50 text-gray-400'
                  }`}>
                  {device.status}
                </span>
              </div>
              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-purple-200">Type:</span>
                  <span className="text-white">{device.type}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-purple-200">Protocol:</span>
                  <span className="text-white">{device.protocol}</span>
                </div>
              </div>
              <div className="flex space-x-2">
                <button className="flex-1 bg-purple-700 hover:bg-purple-600 text-white py-2 px-3 rounded-lg text-sm font-medium transition-colors">
                  Configure
                </button>
                <button className="bg-purple-800 hover:bg-purple-700 text-white p-2 rounded-lg transition-colors">
                  <Info className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Connection Tester Component
  const ConnectionTester = () => (
    <div className="space-y-6">
      <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Connection Tester</h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-5">
            <h3 className="text-lg font-semibold text-white mb-4">Test Configuration</h3>

            <div className="space-y-4">
              <div>
                <label className="block text-purple-200 text-sm mb-2">Device Type</label>
                <select className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
                  {deviceTypes.map((type, index) => (
                    <option key={index} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-purple-200 text-sm mb-2">Protocol</label>
                <select className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
                  {protocols.map((protocol, index) => (
                    <option key={index} value={protocol}>{protocol}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-purple-200 text-sm mb-2">IP Address</label>
                <input
                  type="text"
                  placeholder="192.168.1.100"
                  className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-purple-200 text-sm mb-2">Port</label>
                <input
                  type="number"
                  defaultValue="502"
                  className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-purple-200 text-sm mb-2">Timeout (ms)</label>
                <input
                  type="number"
                  defaultValue="5000"
                  className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>

            <button className="w-full mt-6 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-3 rounded-lg font-semibold transition-all flex items-center justify-center">
              <Play className="w-4 h-4 mr-2" />
              Test Connection
            </button>
          </div>

          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-5">
            <h3 className="text-lg font-semibold text-white mb-4">Test Results</h3>

            <div className="space-y-4">
              <div className="backdrop-blur-xl bg-purple-900/30 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-purple-200">Connection Status</span>
                  <span className="text-green-400 font-semibold">Success</span>
                </div>
                <div className="w-full bg-purple-700 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '100%' }}></div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="backdrop-blur-xl bg-purple-900/30 rounded-lg p-3">
                  <div className="text-purple-200 text-sm">Response Time</div>
                  <div className="text-white font-semibold">45ms</div>
                </div>
                <div className="backdrop-blur-xl bg-purple-900/30 rounded-lg p-3">
                  <div className="text-purple-200 text-sm">Data Points</div>
                  <div className="text-white font-semibold">127</div>
                </div>
              </div>

              <div className="backdrop-blur-xl bg-purple-900/30 rounded-lg p-4">
                <div className="text-purple-200 text-sm mb-2">Connection Details</div>
                <div className="text-white text-sm space-y-1">
                  <div>Protocol: Modbus TCP</div>
                  <div>Device: Siemens S7-1200</div>
                  <div>IP: 192.168.1.100:502</div>
                  <div>Connected: Jan 15, 2024 14:30</div>
                </div>
              </div>

              <button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-2 rounded-lg font-semibold transition-all">
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Tag Browser Component
  const TagBrowser = () => (
    <div className="space-y-6">
      <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Tag Browser & Mapping</h2>
          <div className="flex space-x-3">
            <button className="flex items-center space-x-2 bg-purple-700 hover:bg-purple-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
              <RefreshCw className="w-4 h-4" />
              <span>Refresh</span>
            </button>
            <button className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-4 py-2 rounded-lg font-medium transition-all">
              <Plus className="w-4 h-4" />
              <span>Add Mapping</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-5">
            <h3 className="text-lg font-semibold text-white mb-4">Source Tags</h3>

            <div className="flex space-x-3 mb-4">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="Filter tags..."
                  className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <select className="bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
                <option>All Devices</option>
                <option>Siemens S7-1200</option>
                <option>Modbus Device A</option>
              </select>
            </div>

            <div className="max-h-96 overflow-y-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-purple-500/30">
                    <th className="text-left py-2 px-3 text-purple-200 text-sm font-semibold">Tag Name</th>
                    <th className="text-left py-2 px-3 text-purple-200 text-sm font-semibold">Data Type</th>
                    <th className="text-left py-2 px-3 text-purple-200 text-sm font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { name: 'Temperature_Sensor_1', type: 'Float' },
                    { name: 'Pressure_Gauge_1', type: 'Integer' },
                    { name: 'Motor_Status', type: 'Boolean' },
                    { name: 'Flow_Rate', type: 'Double' },
                    { name: 'Valve_Position', type: 'Integer' },
                    { name: 'Alarm_Status', type: 'String' }
                  ].map((tag, index) => (
                    <tr key={index} className="border-b border-purple-500/20 hover:bg-purple-800/20">
                      <td className="py-2 px-3 text-white text-sm">{tag.name}</td>
                      <td className="py-2 px-3 text-purple-200 text-sm">{tag.type}</td>
                      <td className="py-2 px-3">
                        <button className="text-purple-400 hover:text-purple-300">
                          <Map className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-5">
            <h3 className="text-lg font-semibold text-white mb-4">Tag Mappings</h3>

            <div className="max-h-96 overflow-y-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-purple-500/30">
                    <th className="text-left py-2 px-3 text-purple-200 text-sm font-semibold">Source</th>
                    <th className="text-left py-2 px-3 text-purple-200 text-sm font-semibold">Target</th>
                    <th className="text-left py-2 px-3 text-purple-200 text-sm font-semibold">Type</th>
                    <th className="text-left py-2 px-3 text-purple-200 text-sm font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {tagMappings.map((mapping) => (
                    <tr key={mapping.id} className="border-b border-purple-500/20 hover:bg-purple-800/20">
                      <td className="py-2 px-3 text-white text-sm">{mapping.source}</td>
                      <td className="py-2 px-3 text-white text-sm">{mapping.target}</td>
                      <td className="py-2 px-3 text-purple-200 text-sm">{mapping.dataType}</td>
                      <td className="py-2 px-3">
                        <button className="text-purple-400 hover:text-purple-300 mr-2">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button className="text-red-400 hover:text-red-300">
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-4 pt-4 border-t border-purple-500/30">
              <div className="flex justify-between items-center">
                <span className="text-purple-200 text-sm">Total Mappings: {tagMappings.length}</span>
                <button className="flex items-center space-x-1 text-purple-300 hover:text-white text-sm">
                  <Download className="w-4 h-4" />
                  <span>Export</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Protocol Converter Component
  const ProtocolConverter = () => (
    <div className="space-y-6">
      <div className="backdrop-blur-xl bg-gradient-to-br from-purple-900/40 to-indigo-900/40 border border-purple-500/20 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Protocol Converter</h2>
          <button className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-4 py-2 rounded-lg font-semibold transition-all">
            <Plus className="w-4 h-4" />
            <span>New Conversion</span>
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-5">
            <h3 className="text-lg font-semibold text-white mb-4">Source Protocol</h3>
            <select className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 mb-4">
              {protocols.map((protocol, index) => (
                <option key={index} value={protocol}>{protocol}</option>
              ))}
            </select>
            <div className="space-y-3">
              <div>
                <label className="block text-purple-200 text-sm mb-1">IP Address</label>
                <input
                  type="text"
                  placeholder="192.168.1.100"
                  className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-purple-200 text-sm mb-1">Port</label>
                <input
                  type="number"
                  defaultValue="502"
                  className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>
          </div>

          <div className="flex items-center justify-center">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center">
              <ArrowRight className="w-6 h-6 text-white" />
            </div>
          </div>

          <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-5">
            <h3 className="text-lg font-semibold text-white mb-4">Target Protocol</h3>
            <select className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500 mb-4">
              {protocols.map((protocol, index) => (
                <option key={index} value={protocol}>{protocol}</option>
              ))}
            </select>
            <div className="space-y-3">
              <div>
                <label className="block text-purple-200 text-sm mb-1">Broker/Server</label>
                <input
                  type="text"
                  placeholder="mqtt.example.com"
                  className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-purple-200 text-sm mb-1">Topic/Endpoint</label>
                <input
                  type="text"
                  placeholder="/devices/sensor1"
                  className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="backdrop-blur-xl bg-purple-800/30 rounded-xl p-5">
          <h3 className="text-lg font-semibold text-white mb-4">Conversion Rules</h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-purple-200 text-sm mb-2">Data Transformation</label>
              <select className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
                <option>None</option>
                <option>Scale by 10</option>
                <option>Convert Units</option>
                <option>Custom Function</option>
              </select>
            </div>
            <div>
              <label className="block text-purple-200 text-sm mb-2">Update Interval</label>
              <select className="w-full bg-purple-900/50 border border-purple-500/30 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
                <option>Real-time</option>
                <option>1 second</option>
                <option>5 seconds</option>
                <option>30 seconds</option>
                <option>1 minute</option>
              </select>
            </div>
          </div>

          <div className="flex space-x-3">
            <button className="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white py-3 rounded-lg font-semibold transition-all">
              Start Conversion
            </button>
            <button className="bg-purple-700 hover:bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
              Save
            </button>
          </div>
        </div>

        <div className="mt-8">
          <h3 className="text-lg font-semibold text-white mb-4">Active Conversions</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-purple-500/30">
                  <th className="text-left py-3 px-4 text-purple-200 font-semibold">Source</th>
                  <th className="text-left py-3 px-4 text-purple-200 font-semibold">Target</th>
                  <th className="text-left py-3 px-4 text-purple-200 font-semibold">Status</th>
                  <th className="text-left py-3 px-4 text-purple-200 font-semibold">Last Used</th>
                  <th className="text-left py-3 px-4 text-purple-200 font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody>
                {protocolConversions.map((conversion) => (
                  <tr key={conversion.id} className="border-b border-purple-500/20 hover:bg-purple-800/20">
                    <td className="py-3 px-4 text-white">{conversion.source}</td>
                    <td className="py-3 px-4 text-white">{conversion.target}</td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-900/50 text-green-400">
                        <Check className="w-3 h-3 mr-1" />
                        {conversion.status}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-purple-200">{conversion.lastUsed}</td>
                    <td className="py-3 px-4">
                      <button className="text-purple-400 hover:text-purple-300 mr-3">
                        <Play className="w-4 h-4" />
                      </button>
                      <button className="text-red-400 hover:text-red-300">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'discovery': return <AutoDiscovery />;
      case 'library': return <DeviceLibrary />;
      case 'tester': return <ConnectionTester />;
      case 'browser': return <TagBrowser />;
      case 'converter': return <ProtocolConverter />;
      default: return <AutoDiscovery />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="backdrop-blur-xl bg-purple-900/30 border-b border-purple-500/20">
        <div className="container mx-auto px-6 py-6">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-white">Device & Protocol Management</h1>
              <p className="text-purple-200 mt-1">Configure and manage your industrial devices and protocols</p>
            </div>
            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 bg-purple-800 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
                <Save className="w-4 h-4" />
                <span>Save Config</span>
              </button>
              <button className="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-4 py-2 rounded-lg transition-all">
                <Upload className="w-4 h-4" />
                <span>Import</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="backdrop-blur-xl bg-purple-900/20 border-b border-purple-500/20">
        <div className="container mx-auto px-6">
          <div className="flex overflow-x-auto space-x-1 py-3">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg whitespace-nowrap transition-all ${activeTab === tab.id
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                    : 'text-purple-300 hover:text-white hover:bg-purple-800/50'
                  }`}
              >
                {tab.icon}
                <span className="font-medium">{tab.name}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        {renderActiveTab()}
      </div>

      {/* Status Bar */}
      <div className="backdrop-blur-xl bg-purple-900/30 border-t border-purple-500/20 mt-12">
        <div className="container mx-auto px-6 py-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 items-center justify-between text-sm">
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2 text-green-400">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>3 Active Devices</span>
              </div>
              <div className="flex items-center space-x-2 text-blue-400">
                <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                <span>5 Active Conversions</span>
              </div>
              <div className="flex items-center space-x-2 text-purple-400">
                <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                <span>12 Tag Mappings</span>
              </div>
            </div>
            <div className="text-purple-300">
              Last Updated: Jan 15, 2024 14:30
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;