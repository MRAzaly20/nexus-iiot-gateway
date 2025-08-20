"use client";
import React, { useState } from 'react';
import { Eye, EyeOff, Factory, Shield, Zap, Wifi } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function App() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const router = useRouter();
  const [formData, setFormData] = useState({
    companyName: '',
    email: '',
    password: '',
    confirmPassword: '',
    industry: '',
    employeeCount: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  const toLogin = () => {
    console.log("test")
    router.push('/auth/signin');
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    // Handle signup logic here
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-purple-800 flex items-center justify-center p-4">
      {/* Background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-soft-light filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-500 rounded-full mix-blend-soft-light filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-violet-600 rounded-full mix-blend-soft-light filter blur-3xl opacity-20"></div>
      </div>

      {/* Main container */}
      <div className="relative w-full max-w-6xl mx-auto grid lg:grid-cols-2 gap-8 items-center z-10">
        {/* Left side - Branding */}
        <div className="hidden lg:flex flex-col space-y-8 p-12">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-white/10 backdrop-blur-lg rounded-xl border border-white/20">
              <Factory className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white">IndustrialIoT</h1>
          </div>

          <div className="space-y-6">
            <div className="flex items-center space-x-4">
              <div className="p-2 bg-white/10 backdrop-blur-lg rounded-lg border border-white/20">
                <Shield className="h-6 w-6 text-violet-300" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Secure Connectivity</h3>
                <p className="text-purple-200">Enterprise-grade security for your industrial assets</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="p-2 bg-white/10 backdrop-blur-lg rounded-lg border border-white/20">
                <Zap className="h-6 w-6 text-violet-300" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Real-time Monitoring</h3>
                <p className="text-purple-200">Instant insights into your industrial operations</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="p-2 bg-white/10 backdrop-blur-lg rounded-lg border border-white/20">
                <Wifi className="h-6 w-6 text-violet-300" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Seamless Integration</h3>
                <p className="text-purple-200">Connect all your devices with our unified platform</p>
              </div>
            </div>
          </div>

          <div className="mt-8 p-6 bg-white/5 backdrop-blur-lg rounded-xl border border-white/10">
            <blockquote className="text-lg italic text-purple-100">
              "IndustrialIoT has transformed how we monitor and manage our factory operations. The real-time data insights have increased our efficiency by 35%."
            </blockquote>
            <p className="mt-4 text-purple-200 font-medium">- Manufacturing Director, TechCorp Industries</p>
          </div>
        </div>

        {/* Right side - Signup Form */}
        <div className="w-full">
          <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 shadow-2xl p-8 md:p-10">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">Create Your Account</h2>
              <p className="text-purple-200">Join thousands of industrial companies transforming their operations</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="companyName" className="block text-sm font-medium text-purple-100 mb-2">
                    Company Name
                  </label>
                  <input
                    type="text"
                    id="companyName"
                    name="companyName"
                    value={formData.companyName}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent backdrop-blur-sm transition-all"
                    placeholder="Acme Manufacturing"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-purple-100 mb-2">
                    Work Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent backdrop-blur-sm transition-all"
                    placeholder="name@company.com"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="relative">
                  <label htmlFor="password" className="block text-sm font-medium text-purple-100 mb-2">
                    Password
                  </label>
                  <input
                    type={showPassword ? "text" : "password"}
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent backdrop-blur-sm pr-12 transition-all"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-9 text-purple-300 hover:text-white focus:outline-none"
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>

                <div className="relative">
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-purple-100 mb-2">
                    Confirm Password
                  </label>
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent backdrop-blur-sm pr-12 transition-all"
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-9 text-purple-300 hover:text-white focus:outline-none"
                  >
                    {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label htmlFor="industry" className="block text-sm font-medium text-purple-100 mb-2">
                    Industry
                  </label>
                  <select
                    id="industry"
                    name="industry"
                    value={formData.industry}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent backdrop-blur-sm appearance-none transition-all"
                  >
                    <option value="" className="bg-purple-900">Select Industry</option>
                    <option value="manufacturing" className="bg-purple-900">Manufacturing</option>
                    <option value="energy" className="bg-purple-900">Energy & Utilities</option>
                    <option value="automotive" className="bg-purple-900">Automotive</option>
                    <option value="aerospace" className="bg-purple-900">Aerospace</option>
                    <option value="pharmaceutical" className="bg-purple-900">Pharmaceutical</option>
                    <option value="other" className="bg-purple-900">Other</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="employeeCount" className="block text-sm font-medium text-purple-100 mb-2">
                    Employee Count
                  </label>
                  <select
                    id="employeeCount"
                    name="employeeCount"
                    value={formData.employeeCount}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent backdrop-blur-sm appearance-none transition-all"
                  >
                    <option value="" className="bg-purple-900">Select Range</option>
                    <option value="1-50" className="bg-purple-900">1-50 employees</option>
                    <option value="51-200" className="bg-purple-900">51-200 employees</option>
                    <option value="201-1000" className="bg-purple-900">201-1000 employees</option>
                    <option value="1000+" className="bg-purple-900">1000+ employees</option>
                  </select>
                </div>
              </div>

              <div className="flex items-center">
                <input
                  id="terms"
                  type="checkbox"
                  required
                  className="w-4 h-4 text-violet-600 bg-white/10 border-white/20 rounded focus:ring-violet-500 focus:ring-2"
                />
                <label htmlFor="terms" className="ml-2 text-sm text-purple-200">
                  I agree to the <a href="#" className="text-violet-300 hover:text-violet-100 underline">Terms of Service</a> and <a href="#" className="text-violet-300 hover:text-violet-100 underline">Privacy Policy</a>
                </label>
              </div>

              <button
                type="submit"
                className="w-full py-3 px-4 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white font-semibold rounded-lg shadow-lg transform transition-all duration-200 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 focus:ring-offset-transparent"
              >
                Create Account
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-purple-200">
                Already have an account?{' '}
                <input type="button" value="Sign in" onClick={toLogin} className="text-violet-300 hover:text-violet-100 font-medium underline cursor-pointer" />
              </p>
            </div>
          </div>

          <div className="mt-6 text-center text-sm text-purple-300">
            <p>© 2023 IndustrialIoT. All rights reserved.</p>
          </div>
        </div>
      </div>
    </div>
  );
}