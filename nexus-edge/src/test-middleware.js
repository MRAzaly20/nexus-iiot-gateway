// middleware.js
import { NextResponse } from 'next/server'

export function middleware(request) {
  const { pathname } = request.nextUrl
  
  // Izinkan akses ke /features dan sub-path nya
  if (pathname === '/feature' || pathname.startsWith('/feature/')) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  // Izinkan akses ke halaman utama
  if (pathname === '/') {
    return NextResponse.next()
  }

  // Opsional: Izinkan akses ke halaman login/register jika ada
  if (pathname === '/login' || pathname === '/register') {
    return NextResponse.next()
  }

  // Untuk semua path lainnya, redirect ke halaman /
  return NextResponse.redirect(new URL('/', request.url))
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|robots.txt).*)',
  ],
}