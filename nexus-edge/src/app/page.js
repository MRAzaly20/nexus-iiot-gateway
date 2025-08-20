"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession, signIn, signOut } from 'next-auth/react'; // Import useSession and signOut
import { Shield, Cpu, Cloud, Zap, ArrowRight, Menu, X, CheckCircle, Globe, Lock, Activity, User, Mail, Eye, EyeOff } from 'lucide-react';

const NexusEdgeLanding = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrollY, setScrollY] = useState(0);
  const [showLogin, setShowLogin] = useState(false);
  const [showSignup, setShowSignup] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false); // State for profile dropdown
  const router = useRouter();

  // Use NextAuth session hook
  const { data: session, status } = useSession();
  const isAuthenticated = status === "authenticated";
  const isLoadingAuth = status === "loading";

  const [signupForm, setSignupForm] = useState({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    password: '',
    confirmPassword: ''
  });

  const [formErrors, setFormErrors] = useState({});
  const [loginForm, setLoginForm] = useState({
    email: '',
    password: ''
  });

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    const checkIfMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('scroll', handleScroll);
    checkIfMobile();
    window.addEventListener('resize', checkIfMobile);

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', checkIfMobile);
    };
  }, []);

  // Close profile dropdown if clicked outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (isProfileOpen && !event.target.closest('.profile-dropdown')) {
        setIsProfileOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isProfileOpen]);

  const validateForm = (form, isLogin = false) => {
    const errors = {};

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!form.email || !emailRegex.test(form.email)) {
      errors.email = 'Please enter a valid email address';
    }

    if (!form.password || form.password.length < 8) {
      errors.password = 'Password must be at least 8 characters long';
    }

    if (!isLogin) {
      if (!form.firstName || form.firstName.trim().length < 2) {
        errors.firstName = 'First name must be at least 2 characters';
      }
      if (!form.lastName || form.lastName.trim().length < 2) {
        errors.lastName = 'Last name must be at least 2 characters';
      }
      if (!form.company || form.company.trim().length < 2) {
        errors.company = 'Company name is required';
      }
      if (form.password !== form.confirmPassword) {
        errors.confirmPassword = 'Passwords do not match';
      }
    }

    return errors;
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    const errors = validateForm(loginForm, true);

    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setIsLoading(true);
    setFormErrors({});

    try {
      const result = await signIn("credentials", {
        email: loginForm.email,
        password: loginForm.password,
        action: "login",
        redirect: false,
      });
      console.log(result);
      if (result?.error) {
        setFormErrors({ submit: result.error || 'Login failed. Please check your credentials.' });
      } else {
        // Close modal and let useSession update the UI
        closeModal();
        // Optionally, redirect if needed, but useSession should trigger a re-render
        // router.push('/feature');
      }
    } catch (error) {
      setFormErrors({ submit: 'Login failed. Please check your credentials.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    const errors = validateForm(signupForm, false);

    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setIsLoading(true);
    setFormErrors({});

    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: signupForm.email,
          password: signupForm.password,
          firstName: signupForm.firstName,
          lastName: signupForm.lastName,
          // company: signupForm.company // Add if your backend API expects it
        }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log(data.message);
        // Close modal
        closeModal();
        // Trigger login after signup or rely on session update
        // You might want to automatically log the user in after signup
        // Or redirect to a "check your email" page if email verification is added later
        const loginResult = await signIn("credentials", {
          email: signupForm.email,
          password: signupForm.password,
          redirect: false,
        });
        if (!loginResult?.error) {
          
          //router.push('/feature');
        } else {
          setFormErrors({ submit: 'Signup successful, but login failed. Please try logging in.' });
        }
      } else {
        if (response.status === 409) {
          setFormErrors({ submit: data.error || 'Email already in use.' });
        } else if (response.status === 400) {
          setFormErrors({ submit: 'Invalid input. Please check your details.' });
        } else {
          setFormErrors({ submit: data.error || 'Signup failed. Please try again.' });
        }
      }
    } catch (error) {
      console.error("Network or parsing error:", error);
      setFormErrors({ submit: 'Network error. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const closeModal = () => {
    setShowLogin(false);
    setShowSignup(false);
    setFormErrors({});
    setShowPassword(false);
    setShowConfirmPassword(false);
  };

  // Logout function for all providers (Google, GitHub, Credentials)
  const handleLogout = async () => {
    setIsProfileOpen(false); // Close dropdown
    try {
      await signOut({ callbackUrl: '/' }); // Redirect to home or login page after logout
    } catch (error) {
      console.error("Logout error:", error);
      // Optionally show an error message to the user
    }
  };

  // Get user display name
  const getUserDisplayName = () => {
    if (!session?.user) return 'User';
    return session.user.name || session.user.firstName || session.user.email || 'User';
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white overflow-x-hidden">
      {/* Animated Gradient Background - Hidden on mobile */}
      {!isMobile && (
        <div className="fixed inset-0 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-blue-900/20 to-purple-900/20"></div>
          <div className="absolute inset-0">
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-r from-blue-600/30 to-cyan-500/30 rounded-full blur-3xl animate-pulse opacity-70 animate-float-slow"></div>
            <div className="absolute top-1/2 right-1/3 w-80 h-80 bg-gradient-to-r from-purple-600/25 to-pink-500/25 rounded-full blur-3xl opacity-60 animate-float-reverse"></div>
            <div className="absolute bottom-1/4 left-1/2 w-72 h-72 bg-gradient-to-r from-indigo-600/20 to-blue-500/20 rounded-full blur-3xl opacity-50 animate-float-diagonal"></div>
          </div>
          <div className="absolute inset-0 opacity-40">
            <div className="absolute top-10 right-10 w-32 h-32 bg-gradient-to-br from-blue-500/30 to-transparent border border-blue-500/20 backdrop-blur-sm rounded-2xl animate-gradient-shift-1"></div>
            <div className="absolute bottom-20 left-10 w-40 h-40 bg-gradient-to-tr from-purple-500/25 to-transparent border border-purple-500/15 backdrop-blur-sm rounded-2xl animate-gradient-shift-2"></div>
            <div className="absolute top-1/3 left-1/3 w-24 h-24 bg-gradient-to-bl from-cyan-500/30 to-transparent border border-cyan-500/20 backdrop-blur-sm rounded-2xl animate-gradient-shift-3"></div>
          </div>
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(17,24,39,0.7),rgba(17,24,39,0.95))]"></div>
        </div>
      )}

      {/* Custom CSS for animations - only applied when not on mobile */}
      {!isMobile && (
        <style jsx global>{`
          @keyframes float-slow {
            0%, 100% { transform: translateY(0px) translateX(0px) scale(1); }
            25% { transform: translateY(-20px) translateX(10px) scale(1.1); }
            50% { transform: translateY(-10px) translateX(-15px) scale(0.9); }
            75% { transform: translateY(-30px) translateX(5px) scale(1.05); }
          }
          
          @keyframes float-reverse {
            0%, 100% { transform: translateY(0px) translateX(0px) rotate(0deg); }
            33% { transform: translateY(15px) translateX(-20px) rotate(120deg); }
            66% { transform: translateY(-25px) translateX(10px) rotate(240deg); }
          }
          
          @keyframes float-diagonal {
            0%, 100% { transform: translateY(0px) translateX(0px) scale(1); }
            50% { transform: translateY(-40px) translateX(30px) scale(1.2); }
          }
          
          @keyframes gradient-shift-1 {
            0%, 100% { 
              background: linear-gradient(45deg, rgba(59, 130, 246, 0.3), transparent);
              transform: rotate(0deg);
            }
            50% { 
              background: linear-gradient(45deg, rgba(147, 51, 234, 0.3), transparent);
              transform: rotate(180deg);
            }
          }
          
          @keyframes gradient-shift-2 {
            0%, 100% { 
              background: linear-gradient(135deg, rgba(147, 51, 234, 0.25), transparent);
              transform: rotate(0deg) scale(1);
            }
            33% { 
              background: linear-gradient(135deg, rgba(59, 130, 246, 0.25), transparent);
              transform: rotate(120deg) scale(1.1);
            }
            66% { 
              background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), transparent);
              transform: rotate(240deg) scale(0.9);
            }
          }
          
          @keyframes gradient-shift-3 {
            0%, 100% { 
              background: linear-gradient(225deg, rgba(6, 182, 212, 0.3), transparent);
              transform: translateY(0px);
            }
            50% { 
              background: linear-gradient(225deg, rgba(168, 85, 247, 0.3), transparent);
              transform: translateY(-20px);
            }
          }
          
          @keyframes gradient-float-1 {
            0%, 100% { 
              transform: rotate(45deg) translateY(0px) scale(1);
              background: linear-gradient(45deg, rgba(34, 211, 238, 0.2), rgba(59, 130, 246, 0.2));
            }
            50% { 
              transform: rotate(225deg) translateY(-15px) scale(1.1);
              background: linear-gradient(45deg, rgba(59, 130, 246, 0.25), rgba(147, 51, 234, 0.2));
            }
          }
          
          @keyframes gradient-float-2 {
            0%, 100% { 
              transform: translateY(0px) scale(1);
              background: linear-gradient(135deg, rgba(147, 51, 234, 0.25), rgba(236, 72, 153, 0.25));
            }
            33% { 
              transform: translateY(-10px) scale(1.2);
              background: linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(59, 130, 246, 0.2));
            }
            66% { 
              transform: translateY(5px) scale(0.9);
              background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(34, 211, 238, 0.25));
            }
          }
          
          @keyframes gradient-float-3 {
            0%, 100% { 
              transform: translateX(0px) rotate(0deg);
              background: linear-gradient(90deg, rgba(99, 102, 241, 0.2), rgba(147, 51, 234, 0.2));
            }
            50% { 
              transform: translateX(10px) rotate(180deg);
              background: linear-gradient(90deg, rgba(147, 51, 234, 0.25), rgba(168, 85, 247, 0.2));
            }
          }
          
          @keyframes float-gentle {
            0%, 100% { transform: translateY(0px) translateX(0px); }
            33% { transform: translateY(-8px) translateX(5px); }
            66% { transform: translateY(4px) translateX(-3px); }
          }
          
          @keyframes float-reverse-gentle {
            0%, 100% { transform: translateY(0px) translateX(0px) rotate(0deg); }
            50% { transform: translateY(-12px) translateX(-8px) rotate(180deg); }
          }
          
          @keyframes float-diagonal-gentle {
            0%, 100% { transform: translateY(0px) translateX(0px); }
            50% { transform: translateY(-15px) translateX(12px); }
          }
          
          .animate-float-slow { animation: float-slow 8s ease-in-out infinite; }
          .animate-float-reverse { animation: float-reverse 12s ease-in-out infinite reverse; }
          .animate-float-diagonal { animation: float-diagonal 10s ease-in-out infinite; }
          .animate-gradient-shift-1 { animation: gradient-shift-1 6s ease-in-out infinite; }
          .animate-gradient-shift-2 { animation: gradient-shift-2 9s ease-in-out infinite; }
          .animate-gradient-shift-3 { animation: gradient-shift-3 7s ease-in-out infinite; }
          .animate-gradient-float-1 { animation: gradient-float-1 8s ease-in-out infinite; }
          .animate-gradient-float-2 { animation: gradient-float-2 6s ease-in-out infinite; }
          .animate-gradient-float-3 { animation: gradient-float-3 10s ease-in-out infinite; }
          .animate-float-gentle { animation: float-gentle 6s ease-in-out infinite; }
          .animate-float-reverse-gentle { animation: float-reverse-gentle 8s ease-in-out infinite; }
          .animate-float-diagonal-gentle { animation: float-diagonal-gentle 7s ease-in-out infinite; }
        `}</style>
      )}

      {/* Header */}
      <header className="relative z-50 backdrop-blur-xl bg-white/5 border-b border-white/10">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Cpu className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                NexusEdge
              </span>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="/feature" className="text-gray-300 hover:text-white transition-colors">Features</a>
              <a href="#security" className="text-gray-300 hover:text-white transition-colors">Security</a>
              <a href="#integration" className="text-gray-300 hover:text-white transition-colors">Integration</a>

              {/* Conditional rendering based on auth state */}
              {isLoadingAuth ? (
                <div className="h-8 w-8 rounded-full bg-gray-700 animate-pulse"></div> // Loading indicator
              ) : isAuthenticated && session?.user ? (
                // User is logged in - show profile dropdown
                <div className="relative profile-dropdown">
                  <button
                    onClick={() => setIsProfileOpen(!isProfileOpen)}
                    className="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors focus:outline-none"
                    aria-haspopup="true"
                    aria-expanded={isProfileOpen}
                  >
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                      <User className="w-4 h-4 text-white" />
                    </div>
                    <span className="font-medium hidden lg:inline">{getUserDisplayName()}</span> {/* Optional: hide name on smaller screens */}
                  </button>

                  {/* Dropdown Menu */}
                  {isProfileOpen && (
                    <div className="absolute right-0 mt-2 w-64 bg-gray-800 border border-gray-700 rounded-lg shadow-lg py-2 z-50">
                      <div className="px-4 py-2 border-b border-gray-700">
                        <p className="text-sm font-medium text-white truncate">{session.user.name || `${session.user.firstName} ${session.user.lastName}`}</p>
                        <p className="text-xs text-gray-400 truncate">{session.user.email}</p>
                      </div>
                      <button
                        onClick={handleLogout}
                        className="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 hover:text-white transition-colors flex items-center"
                      >
                        <span>Logout</span>
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                // User is not logged in - show login/signup buttons
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => setShowLogin(true)}
                    className="text-gray-300 hover:text-white transition-colors font-medium"
                  >
                    Login
                  </button>
                  <button
                    onClick={() => setShowSignup(true)}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-6 py-2 rounded-lg font-medium transition-all transform hover:scale-105"
                  >
                    Sign Up
                  </button>
                </div>
              )}
            </div>

            {/* Mobile menu button */}
            <button
              className="md:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden py-4 px-4 backdrop-blur-xl bg-transparent border-t border-white/10">
              <div className="flex flex-col space-y-4">
                <a href="/feature" className="text-gray-300 hover:text-white transition-colors">Features</a>
                <a href="#security" className="text-gray-300 hover:text-white transition-colors">Security</a>
                <a href="#integration" className="text-gray-300 hover:text-white transition-colors">Integration</a>

                {/* Mobile Auth Buttons/Dropdown */}
                {isLoadingAuth ? (
                  <div className="h-8 w-8 rounded-full bg-gray-700 animate-pulse self-start"></div>
                ) : isAuthenticated && session?.user ? (
                  <div className="profile-dropdown">
                    <div className="flex items-center justify-between py-2">
                      <div className="flex items-center space-x-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                          <User className="w-4 h-4 text-white" />
                        </div>
                        <div>
                          <p className="text-sm font-medium text-white">{getUserDisplayName()}</p>
                          <p className="text-xs text-gray-400 truncate">{session.user.email}</p>
                        </div>
                      </div>
                      <button
                        onClick={handleLogout}
                        className="text-xs bg-red-600 hover:bg-red-700 px-3 py-1 rounded"
                      >
                        Logout
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="flex flex-col space-y-2 pt-2">
                    <button
                      onClick={() => {
                        setShowLogin(true);
                        setIsMenuOpen(false); // Close menu on click
                      }}
                      className="text-gray-300 hover:text-white transition-colors font-medium text-left py-2"
                    >
                      Login
                    </button>
                    <button
                      onClick={() => {
                        setShowSignup(true);
                        setIsMenuOpen(false); // Close menu on click
                      }}
                      className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-2 rounded-lg font-medium w-fit"
                    >
                      Sign Up
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </nav>
      </header>

      {/* Hero Section */}
      <section className="relative z-10 pt-20 md:pt-45 pb-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div
            className="transform transition-all duration-1000"
            style={{ transform: `translateY(${scrollY * 0.1}px)` }}
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
              Industrial IoT
              <br />
              <span className="text-white">Gateway Platform</span>
            </h1>
            <p className="text-xl text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
              Connect your edge devices to cloud services with enterprise-grade security.
              Real-time data processing, seamless integration, and bulletproof protocols.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <button
                onClick={() => setShowSignup(true)}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8 py-4 rounded-lg font-bold text-lg transition-all transform hover:scale-105 flex items-center space-x-2"
              >
                <span>Start Integration</span>
                <ArrowRight className="w-5 h-5" />
              </button>
              <button className="backdrop-blur-xl bg-white/10 hover:bg-white/20 border border-white/20 px-8 py-4 rounded-lg font-medium text-lg transition-all">
                View Documentation
              </button>
            </div>
          </div>
        </div>

        {/* Enhanced Floating Elements - Hidden on mobile */}
        {!isMobile && (
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            {/* Animated gradient orbs that respond to scroll */}
            <div
              className="absolute top-1/4 left-1/4 w-32 h-32 bg-gradient-to-r from-blue-500/30 to-cyan-400/30 rounded-full blur-2xl animate-float-gentle"
              style={{ transform: `translateY(${scrollY * 0.05}px) translateX(${Math.sin(scrollY * 0.01) * 10}px)` }}
            ></div>
            <div
              className="absolute top-1/3 right-1/3 w-40 h-40 bg-gradient-to-br from-purple-500/25 to-pink-400/25 rounded-full blur-2xl animate-float-reverse-gentle"
              style={{ transform: `translateY(${scrollY * -0.03}px) translateX(${Math.cos(scrollY * 0.008) * 15}px)` }}
            ></div>
            <div
              className="absolute bottom-1/4 left-1/2 w-28 h-28 bg-gradient-to-l from-indigo-500/30 to-blue-400/30 rounded-full blur-2xl animate-float-diagonal-gentle"
              style={{ transform: `translateY(${scrollY * 0.04}px) translateX(${Math.sin(scrollY * 0.012) * 12}px)` }}
            ></div>

            {/* Floating geometric shapes with gradients */}
            <div className="absolute top-16 right-1/4 w-16 h-16 bg-gradient-to-br from-cyan-400/20 to-blue-600/20 border border-cyan-400/30 backdrop-blur-sm rounded-lg rotate-45 animate-gradient-float-1"></div>
            <div className="absolute bottom-32 right-16 w-12 h-12 bg-gradient-to-tl from-purple-400/25 to-pink-500/25 border border-purple-400/30 backdrop-blur-sm rounded-full animate-gradient-float-2"></div>
            <div className="absolute top-1/2 left-16 w-20 h-20 bg-gradient-to-r from-indigo-400/20 to-purple-500/20 border border-indigo-400/30 backdrop-blur-sm rounded-2xl animate-gradient-float-3"></div>
          </div>
        )}
      </section>

      {/* Features Section */}
      <section id="features" className="relative z-10 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Enterprise-Grade Features
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Built for mission-critical industrial environments with zero-compromise reliability
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <Shield className="w-8 h-8" />,
                title: "Military-Grade Security",
                description: "End-to-end encryption, certificate-based authentication, and secure boot protocols protect your industrial data from any threat."
              },
              {
                icon: <Zap className="w-8 h-8" />,
                title: "Real-Time Processing",
                description: "Sub-millisecond latency edge computing ensures your critical systems respond instantly to changing conditions."
              },
              {
                icon: <Cloud className="w-8 h-8" />,
                title: "Seamless Cloud Integration",
                description: "Native support for AWS IoT, Azure IoT Hub, Google Cloud IoT, and private cloud deployments."
              },
              {
                icon: <Activity className="w-8 h-8" />,
                title: "Advanced Analytics",
                description: "Built-in machine learning pipelines detect anomalies and predict maintenance needs before failures occur."
              },
              {
                icon: <Globe className="w-8 h-8" />,
                title: "Global Scalability",
                description: "Deploy across continents with automatic failover and load balancing for 99.99% uptime guarantee."
              },
              {
                icon: <Lock className="w-8 h-8" />,
                title: "Compliance Ready",
                description: "Pre-configured for ISO 27001, SOC 2, and industrial standards including IEC 62443 cybersecurity frameworks."
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all duration-300 transform hover:-translate-y-2"
              >
                <div className="bg-gradient-to-r from-blue-500 to-purple-600 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-4 text-white">{feature.title}</h3>
                <p className="text-gray-300 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Security Section */}
      <section id="security" className="relative z-10 py-20 bg-gradient-to-r from-blue-900/20 to-purple-900/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Zero-Trust Security Architecture
              </h2>
              <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                Every connection is verified, every packet is inspected, and every device is authenticated.
                Our security model assumes breach and validates everything.
              </p>

              <div className="space-y-4">
                {[
                  "Hardware Security Module (HSM) integration",
                  "Mutual TLS authentication for all connections",
                  "Real-time threat detection and response",
                  "Encrypted data at rest and in transit",
                  "Role-based access control (RBAC)",
                  "Audit logging with tamper-proof storage"
                ].map((item, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-400 flex-shrink-0" />
                    <span className="text-gray-300">{item}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-2xl p-8">
              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-green-500/20 rounded-lg border border-green-500/30">
                  <span className="text-green-300">Security Status</span>
                  <span className="text-green-400 font-bold">SECURE</span>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 backdrop-blur bg-white/5 rounded-lg">
                    <div className="text-2xl font-bold text-blue-400">256-bit</div>
                    <div className="text-sm text-gray-400">AES Encryption</div>
                  </div>
                  <div className="p-4 backdrop-blur bg-white/5 rounded-lg">
                    <div className="text-2xl font-bold text-purple-400">99.99%</div>
                    <div className="text-sm text-gray-400">Uptime SLA</div>
                  </div>
                  <div className="p-4 backdrop-blur bg-white/5 rounded-lg">
                    <div className="text-2xl font-bold text-cyan-400">1ms</div>
                    <div className="text-sm text-gray-400">Response Time</div>
                  </div>
                  <div className="p-4 backdrop-blur bg-white/5 rounded-lg">
                    <div className="text-2xl font-bold text-green-400">24/7</div>
                    <div className="text-sm text-gray-400">Monitoring</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="backdrop-blur-xl bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-white/20 rounded-3xl p-12">
            <h2 className="text-4xl font-bold mb-6 text-white">
              Ready to Transform Your Industrial Operations?
            </h2>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Join industry leaders who trust NexusEdge to connect their critical infrastructure to the future.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={() => setShowSignup(true)}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8 py-4 rounded-lg font-bold text-lg transition-all transform hover:scale-105"
              >
                Start Free Trial
              </button>
              <button className="backdrop-blur-xl bg-white/10 hover:bg-white/20 border border-white/20 px-8 py-4 rounded-lg font-medium text-lg transition-all">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="col-span-1">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Cpu className="w-5 h-5 text-white" />
                </div>
                <span className="text-lg font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  NexusEdge
                </span>
              </div>
              <p className="text-gray-400 text-sm">
                Industrial IoT gateway platform for the modern enterprise.
              </p>
            </div>

            <div>
              <h4 className="font-bold text-white mb-4">Product</h4>
              <div className="space-y-2">
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Features</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Security</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Integration</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Pricing</a>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-white mb-4">Company</h4>
              <div className="space-y-2">
                <a href="#" className="text-gray-400 hover:text-white text-sm block">About</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Careers</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Contact</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Blog</a>
              </div>
            </div>

            <div>
              <h4 className="font-bold text-white mb-4">Support</h4>
              <div className="space-y-2">
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Documentation</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Help Center</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Community</a>
                <a href="#" className="text-gray-400 hover:text-white text-sm block">Status</a>
              </div>
            </div>
          </div>

          <div className="border-t border-white/10 mt-8 pt-8 text-center">
            <p className="text-gray-400 text-sm">
              © 2024 NexusEdge IIoT Gateway. All rights reserved.
            </p>
          </div>
        </div>
      </footer>

      {/* Login Modal */}
      {showLogin && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="max-w-md w-full backdrop-blur-xl bg-gray-900/95 border border-white/20 rounded-2xl p-8 relative">
            <button
              onClick={closeModal}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>

            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <User className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Welcome Back</h2>
              <p className="text-gray-400">Sign in to your NexusEdge account</p>
            </div>

            <form onSubmit={handleLogin} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    value={loginForm.email}
                    onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                    className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Enter your email"
                    required
                  />
                </div>
                {formErrors.email && <p className="text-red-400 text-sm mt-1">{formErrors.email}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={loginForm.password}
                    onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                    className="w-full pl-10 pr-12 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {formErrors.password && <p className="text-red-400 text-sm mt-1">{formErrors.password}</p>}
              </div>

              <div className="flex items-center justify-between">
                <label className="flex items-center">
                  <input type="checkbox" className="mr-2 rounded border-gray-300" />
                  <span className="text-sm text-gray-400">Remember me</span>
                </label>
                <a href="#" className="text-sm text-blue-400 hover:text-blue-300 transition-colors">
                  Forgot password?
                </a>
              </div>

              {formErrors.submit && <p className="text-red-400 text-sm">{formErrors.submit}</p>}

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-lg font-bold text-white transition-all transform hover:scale-105"
              >
                {isLoading ? 'Signing In...' : 'Sign In'}
              </button>

              <div className="text-center">
                <span className="text-gray-400">Don't have an account? </span>
                <button
                  type="button"
                  onClick={() => {
                    setShowLogin(false);
                    setShowSignup(true);
                  }}
                  className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
                >
                  Sign up
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Sign Up Modal */}
      {showSignup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="max-w-md w-full backdrop-blur-xl bg-gray-900/95 border border-white/20 rounded-2xl p-8 relative max-h-[90vh] overflow-y-auto">
            <button
              onClick={closeModal}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>

            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                <User className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">Create Account</h2>
              <p className="text-gray-400">Join NexusEdge to get started</p>
            </div>

            <form onSubmit={handleSignup} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">First Name</label>
                  <input
                    type="text"
                    value={signupForm.firstName}
                    onChange={(e) => setSignupForm({ ...signupForm, firstName: e.target.value })}
                    className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="John"
                    required
                  />
                  {formErrors.firstName && <p className="text-red-400 text-xs mt-1">{formErrors.firstName}</p>}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">Last Name</label>
                  <input
                    type="text"
                    value={signupForm.lastName}
                    onChange={(e) => setSignupForm({ ...signupForm, lastName: e.target.value })}
                    className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Doe"
                    required
                  />
                  {formErrors.lastName && <p className="text-red-400 text-xs mt-1">{formErrors.lastName}</p>}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Email Address</label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="email"
                    value={signupForm.email}
                    onChange={(e) => setSignupForm({ ...signupForm, email: e.target.value })}
                    className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="john@company.com"
                    required
                  />
                </div>
                {formErrors.email && <p className="text-red-400 text-sm mt-1">{formErrors.email}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Company</label>
                <input
                  type="text"
                  value={signupForm.company}
                  onChange={(e) => setSignupForm({ ...signupForm, company: e.target.value })}
                  className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 transition-colors"
                  placeholder="Your Company Name"
                  required
                />
                {formErrors.company && <p className="text-red-400 text-sm mt-1">{formErrors.company}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={signupForm.password}
                    onChange={(e) => setSignupForm({ ...signupForm, password: e.target.value })}
                    className="w-full pl-10 pr-12 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Create a strong password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {formErrors.password && <p className="text-red-400 text-sm mt-1">{formErrors.password}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Confirm Password</label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    value={signupForm.confirmPassword}
                    onChange={(e) => setSignupForm({ ...signupForm, confirmPassword: e.target.value })}
                    className="w-full pl-10 pr-12 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 transition-colors"
                    placeholder="Confirm your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                  >
                    {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
                {formErrors.confirmPassword && <p className="text-red-400 text-sm mt-1">{formErrors.confirmPassword}</p>}
              </div>

              <div className="flex items-start space-x-3">
                <input type="checkbox" required className="mt-1 rounded border-gray-300" />
                <label className="text-sm text-gray-400">
                  I agree to the <a href="#" className="text-blue-400 hover:text-blue-300">Terms of Service</a> and
                  <a href="#" className="text-blue-400 hover:text-blue-300"> Privacy Policy</a>
                </label>
              </div>

              {formErrors.submit && <p className="text-red-400 text-sm">{formErrors.submit}</p>}

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-lg font-bold text-white transition-all transform hover:scale-105"
              >
                {isLoading ? 'Creating Account...' : 'Create Account'}
              </button>

              <div className="text-center">
                <span className="text-gray-400">Already have an account? </span>
                <button
                  type="button"
                  onClick={() => {
                    setShowSignup(false);
                    setShowLogin(true);
                  }}
                  className="text-blue-400 hover:text-blue-300 font-medium transition-colors"
                >
                  Sign in
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default NexusEdgeLanding;