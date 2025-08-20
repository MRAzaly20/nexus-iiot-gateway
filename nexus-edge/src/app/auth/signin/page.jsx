"use client";
import React, { useState } from 'react';
import { Eye, EyeOff, Factory, Shield, Zap, Wifi } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { signIn } from 'next-auth/react';


export default function App() {
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  const toSignup = () => {
    router.push('/auth/signup');
  };
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Login submitted:', formData);
    // Handle login logic here
  };
  const handleSocialLogin = (provider) => {
    setLoading(true);
    signIn(provider, { callbackUrl: '/feature' });
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

        {/* Right side - Login Form */}
        <div className="w-full">
          <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 shadow-2xl p-8 md:p-10">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">Welcome Back</h2>
              <p className="text-purple-200">Sign in to access your industrial dashboard</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
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

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="remember"
                    type="checkbox"
                    className="w-4 h-4 text-violet-600 bg-white/10 border-white/20 rounded focus:ring-violet-500 focus:ring-2"
                  />
                  <label htmlFor="remember" className="ml-2 text-sm text-purple-200">
                    Remember me
                  </label>
                </div>
                <a href="#" className="text-sm text-violet-300 hover:text-violet-100 font-medium">
                  Forgot password?
                </a>
              </div>

              <button
                type="submit"
                className="w-full py-3 px-4 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white font-semibold rounded-lg shadow-lg transform transition-all duration-200 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 focus:ring-offset-transparent"
              >
                Sign In
              </button>
            </form>

            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-white/20"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-transparent text-purple-300">Or continue with</span>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-2 gap-3">
                <button
                  type="button"
                  className="w-full inline-flex justify-center py-2 px-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-md shadow-sm text-sm font-medium text-white hover:bg-white/20 transition-all"
                  onClick={() => handleSocialLogin('google')}
                >
                  <svg className="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12.24 10.285V14.4h6.806c-.275 1.765-2.056 5.174-6.806 5.174-4.095 0-7.439-3.389-7.439-7.574s3.345-7.574 7.439-7.574c2.33 0 3.891.989 4.785 1.849l3.254-3.138C18.189 1.186 15.479 0 12.24 0c-6.635 0-12 5.365-12 12s5.365 12 12 12c6.926 0 11.52-4.869 11.52-11.726 0-.788-.085-1.39-.189-1.989H12.24z" />
                  </svg>
                  <span className="ml-2">Google</span>
                </button>
                <button
                  type="button"
                  className="w-full inline-flex justify-center py-2 px-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-md shadow-sm text-sm font-medium text-white hover:bg-white/20 transition-all"
                  onClick={() => handleSocialLogin('github')}
                >
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                  </svg>
                  <span className="ml-2">GitHub</span>
                </button>
              </div>
            </div>

            <div className="mt-6 text-center">
              <p className="text-purple-200">
                Don't have an account?{' '}
                <input type="button" value="Sign Up" onClick={toSignup} className="ml-2 text-violet-300 hover:text-violet-100 font-medium underline cursor-pointer" />
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