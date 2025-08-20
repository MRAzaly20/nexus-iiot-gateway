"use client";

import React, { useState, useEffect } from 'react';
import { Check, X, ArrowRight, Shield, Wifi, Cloud, Zap, Server } from 'lucide-react';

const App = () => {
  const [selectedPlan, setSelectedPlan] = useState('professional');
  const [snapLoaded, setSnapLoaded] = useState(false);
  const [processing, setProcessing] = useState({});

  // Load Midtrans Snap JS
  useEffect(() => {
    const midtransScriptUrl = process.env.NODE_ENV === 'production'
      ? 'https://app.midtrans.com/snap/snap.js'
      : 'https://app.sandbox.midtrans.com/snap/snap.js';
    console.log(midtransScriptUrl)
    const script = document.createElement('script');
    script.src = midtransScriptUrl;
    script.async = true;
    script.setAttribute('data-client-key', process.env.NEXT_PUBLIC_MIDTRANS_CLIENT_KEY);
    script.onload = () => setSnapLoaded(true);
    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const plans = [
    {
      id: 'starter',
      name: 'Starter Edge',
      price: 49,
      period: 'per month',
      description: 'Perfect for small-scale deployments and testing',
      features: [
        '5 Device Connections',
        'Basic Security Protocols',
        '1 Cloud Integration',
        '24/7 Community Support',
        '100MB Data Transfer',
        'Standard Updates'
      ],
      notIncluded: [
        'Advanced Analytics',
        'Custom API Access',
        'Priority Support'
      ],
      icon: <Wifi className="w-6 h-6" />,
      color: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      id: 'professional',
      name: 'Professional Edge',
      price: 149,
      period: 'per month',
      description: 'Ideal for medium businesses with growing needs',
      features: [
        '25 Device Connections',
        'Enhanced Security Suite',
        '5 Cloud Integrations',
        'Priority Email Support',
        '1GB Data Transfer',
        'Advanced Analytics',
        'Custom API Access'
      ],
      notIncluded: [
        '24/7 Phone Support',
        'Dedicated Account Manager'
      ],
      icon: <Shield className="w-6 h-6" />,
      color: 'from-purple-500/20 to-pink-500/20',
      popular: true
    },
    {
      id: 'enterprise',
      name: 'Enterprise Edge',
      price: 399,
      period: 'per month',
      description: 'For large organizations with complex requirements',
      features: [
        '100 Device Connections',
        'Military-Grade Encryption',
        'Unlimited Cloud Integrations',
        '24/7 Phone & Email Support',
        '10GB Data Transfer',
        'Real-time Analytics',
        'Custom API & SDK',
        'Dedicated Account Manager'
      ],
      notIncluded: [
        'On-premise Deployment',
        'Custom SLA'
      ],
      icon: <Server className="w-6 h-6" />,
      color: 'from-green-500/20 to-emerald-500/20'
    },
    {
      id: 'industrial',
      name: 'Industrial Edge',
      price: 899,
      period: 'per month',
      description: 'For mission-critical industrial applications',
      features: [
        '500 Device Connections',
        'Quantum-Resistant Security',
        'Multi-Cloud Architecture',
        '24/7 Premium Support',
        '50GB Data Transfer',
        'AI-Powered Analytics',
        'Full API Suite',
        'Senior Account Manager',
        'On-premise Deployment Option'
      ],
      notIncluded: [
        'Custom Hardware Integration'
      ],
      icon: <Zap className="w-6 h-6" />,
      color: 'from-orange-500/20 to-red-500/20'
    },
    {
      id: 'custom',
      name: 'NexusEdge Custom',
      price: null,
      period: 'us',
      description: 'Tailored solutions for unique requirements',
      features: [
        'Unlimited Device Connections',
        'Bespoke Security Framework',
        'Custom Cloud Architecture',
        'White-Glove Support',
        'Unlimited Data Transfer',
        'AI/ML Integration',
        'Complete API Control',
        'Executive Account Manager',
        'Full Customization',
        'SLA Negotiation'
      ],
      notIncluded: [],
      icon: <Cloud className="w-6 h-6" />,
      color: 'from-indigo-500/20 to-purple-500/20'
    }
  ];

  const handlePayment = async (plan) => {
    if (!snapLoaded) {
      alert('Payment system is still loading. Please try again.');
      return;
    }

    if (plan.id === 'custom') {
      window.location.href = 'mailto:sales@nexusedge.com?subject=Custom Plan Inquiry';
      return;
    }

    setProcessing(prev => ({ ...prev, [plan.id]: true }));

    try {
      // Create order ID
      const orderId = `NE-${plan.id.toUpperCase()}-${Date.now()}`;

      // Customer details (in real app, get from session)
      const customerDetails = {
        first_name: 'NexusEdge',
        last_name: 'Customer',
        email: 'muhammadrazalyy@gmail.com',
        phone: '+628123456789'
      };

      // Create transaction on backend
      const response = await fetch('/api/payment/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          orderId,
          grossAmount: plan.price * 1000, // Convert to IDR (assuming price is in USD)
          customerDetails,
          planId: plan.id
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to create payment');
      }
      const snapToken = data.token;
      console.log("Attempting to pay with token:", snapToken);
      if (!snapToken) {
        console.error("No Snap token received from backend!");
        alert("Failed to initiate payment. Please try again.");
        setProcessing(prev => ({ ...prev, [plan.id]: false }));
        return;
      }
      // Redirect to Midtrans payment page
      window.snap.pay(snapToken, {
        // onSuccess: function (result) {
        //   console.log('Payment Success:', result);
        //   alert('Payment successful! Thank you for choosing NexusEdge.');
        //   setProcessing(prev => ({ ...prev, [plan.id]: false }));
        // },
        onPending: function (result) {
          console.log('Payment Pending:', result);
          alert('Payment is being processed. We will notify you once completed.');
          setProcessing(prev => ({ ...prev, [plan.id]: false }));
        },
        onError: function (result) {
          console.error('Payment Error:', result);
          alert('Payment failed or was cancelled.');
          setProcessing(prev => ({ ...prev, [plan.id]: false }));
        },
        onClose: function () {
          console.log('Payment Popup Closed');
          setProcessing(prev => ({ ...prev, [plan.id]: false }));
        }
      });

    } catch (error) {
      console.error('Payment initiation error:', error);
      alert('Failed to initiate payment. Please try again.');
      setProcessing(prev => ({ ...prev, [plan.id]: false }));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      {/* Header */}
      <div className="container mx-auto px-6 py-8">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            NexusEdge IIoT Gateway
          </h1>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Industrial IoT gateway platform connecting edge devices to cloud services with secure protocols.
            Choose the perfect plan for your industrial automation needs.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 max-w-7xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative backdrop-blur-xl bg-gradient-to-br ${plan.color} border border-white/10 rounded-2xl p-8 transition-all duration-300 hover:scale-105 hover:border-white/20 ${selectedPlan === plan.id ? 'ring-2 ring-blue-400 shadow-2xl shadow-blue-400/20' : ''
                } ${plan.popular ? 'ring-2 ring-purple-400 shadow-2xl shadow-purple-400/20' : ''}`}
              onClick={() => setSelectedPlan(plan.id)}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    Most Popular
                  </div>
                </div>
              )}

              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-white/10 mb-4">
                  {plan.icon}
                </div>
                <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                <p className="text-slate-300 text-sm mb-4">{plan.description}</p>
                <div className="flex items-baseline justify-center">
                  <span className="text-4xl font-bold">
                    {plan.price ? `$${plan.price}` : 'Contact'}
                  </span>
                  {plan.price && (
                    <span className="text-slate-400 ml-2">{plan.period}</span>
                  )}
                </div>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-center">
                    <Check className="w-5 h-5 text-green-400 mr-3 flex-shrink-0" />
                    <span className="text-slate-200">{feature}</span>
                  </li>
                ))}
                {plan.notIncluded.map((feature, index) => (
                  <li key={index} className="flex items-center opacity-50">
                    <X className="w-5 h-5 text-red-400 mr-3 flex-shrink-0" />
                    <span className="text-slate-400 line-through">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handlePayment(plan);
                }}
                disabled={processing[plan.id] || (plan.id !== 'custom' && !snapLoaded)}
                className={`w-full py-3 px-6 rounded-xl font-semibold transition-all duration-300 flex items-center justify-center ${selectedPlan === plan.id
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                    : 'bg-white/10 text-white hover:bg-white/20'
                  } ${plan.popular ? 'bg-gradient-to-r from-purple-500 to-pink-500' : ''} ${processing[plan.id] ? 'opacity-70 cursor-not-allowed' : ''
                  }`}
              >
                {processing[plan.id] ? (
                  'Processing...'
                ) : plan.id === 'custom' ? (
                  'Contact Sales'
                ) : (
                  <>
                    Select Plan
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </>
                )}
              </button>
            </div>
          ))}
        </div>

        {/* Features Comparison */}
        <div className="mt-20 backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl p-8">
          <h2 className="text-3xl font-bold text-center mb-12">Platform Features Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <Shield className="w-12 h-12 text-blue-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Military-Grade Security</h3>
              <p className="text-slate-300">End-to-end encryption and secure boot protocols</p>
            </div>
            <div className="text-center">
              <Wifi className="w-12 h-12 text-green-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Multi-Protocol Support</h3>
              <p className="text-slate-300">MQTT, CoAP, HTTP/HTTPS, and industrial protocols</p>
            </div>
            <div className="text-center">
              <Cloud className="w-12 h-12 text-purple-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Cloud Agnostic</h3>
              <p className="text-slate-300">Seamless integration with AWS, Azure, Google Cloud</p>
            </div>
            <div className="text-center">
              <Zap className="w-12 h-12 text-orange-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Edge Computing</h3>
              <p className="text-slate-300">Real-time data processing and analytics at the edge</p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-16 text-center">
          <div className="backdrop-blur-xl bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-white/10 rounded-2xl p-12">
            <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Industrial Operations?</h2>
            <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
              Join thousands of industrial companies leveraging NexusEdge for secure, scalable IoT deployments.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-8 py-4 rounded-xl font-semibold hover:shadow-lg transition-all duration-300">
                Start Free Trial
              </button>
              <button className="border border-white/20 text-white px-8 py-4 rounded-xl font-semibold hover:bg-white/10 transition-all duration-300">
                Schedule Demo
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;