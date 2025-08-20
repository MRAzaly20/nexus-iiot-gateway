// app/api/payment/webhook/route.js
import { NextResponse } from 'next/server';
import crypto from 'crypto';
// import { prisma } from '@/lib/prisma'; // Uncomment jika Anda sudah mengintegrasikan database

// Helper function to verify Midtrans signature
function verifySignature(body, headers, serverKey) {
  const signature = headers.get('x-signature');

  if (!signature) {
    console.warn('No x-signature header found in webhook request.');
    return true;
  }

  try {
    // Create signature using SHA512
    // --- PERBAIKAN UTAMA: Gunakan MIDTRANS_SERVER_KEY, bukan NEXT_PUBLIC_SECRET ---
    const expectedSignature = crypto
      .createHmac('sha512', serverKey) // <-- Gunakan serverKey dari parameter
      .update(body)
      .digest('hex');

    const isValid = signature === expectedSignature;
    if (!isValid) {
      console.warn('Webhook signature mismatch.');
      console.debug('Received signature:', signature);
      // Jangan log expectedSignature secara langsung di produksi karena mengandung secret
      console.debug('Signature verification result:', isValid);
    }
    return isValid;
  } catch (err) {
    console.error('Error during signature verification:', err);
    return false;
  }
}

// Helper function to update user subscription in database
async function updateUserSubscription(orderId, status, transactionData) {
  try {
    // Extract user and plan info from order ID or transaction data
    const orderParts = orderId.split('-');
    const planId = orderParts[1]?.toLowerCase(); 
    
    console.log(`Updating subscription for order ${orderId}: Status=${status}, Plan=${planId}`);
    
    // --- TODO: Implementasi database Anda di sini ---
    // Contoh (hapus komentar dan sesuaikan):
    /*
    if (status === 'settlement' || status === 'capture') {
      // Aktifkan langganan pengguna
       await prisma.subscription.upsert({
         where: { orderId: orderId },
         update: { 
           status: 'ACTIVE',
           expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // Misalnya 30 hari
         },
         create: {
           orderId: orderId,
           planId: planId,
           status: 'ACTIVE',
           // Anda perlu mengaitkan dengan user, misalnya melalui email dari transactionData
           // userId: ... 
           expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
         }
       });
    } else if (status === 'cancel' || status === 'expire' || status === 'deny') {
      // Nonaktifkan langganan
       await prisma.subscription.updateMany({
         where: { orderId: orderId },
         data: { status: 'INACTIVE' }
       });
    }
    */
    // --- Akhir TODO ---

    return true;
  } catch (error) {
    console.error(`Database update error for order ${orderId}:`, error);
    // Pertimbangkan untuk menggunakan sistem logging yang lebih robust seperti Winston
    return false;
  }
}

// Helper function to send confirmation emails (implement as needed)
async function sendConfirmationEmail(transactionData) {
  try {
    const orderId = transactionData.order_id;
    const email = transactionData.customer_details?.email;
    if (!email) {
       console.warn(`No email found in transaction data for order ${orderId}`);
       return;
    }
    console.log(`Sending confirmation email for order ${orderId} to ${email}`);
    // --- TODO: Implementasi pengiriman email Anda di sini ---
    // Contoh menggunakan nodemailer atau layanan email lainnya
    // ...
    // --- Akhir TODO ---
  } catch (error) {
    const orderId = transactionData?.order_id || 'Unknown';
    console.error(`Failed to send confirmation email for order ${orderId}:`, error);
  }
}

export async function POST(request) {
  console.log('Webhook POST request received');
  
  // 1. Pastikan environment variable ada
  const serverKey = process.env.MIDTRANS_SERVER_KEY;
  if (!serverKey) {
    console.error('MIDTRANS_SERVER_KEY is not set in environment variables.');
    // Mengembalikan 500 karena ini adalah kesalahan konfigurasi server
    return NextResponse.json({ error: 'Server configuration error' }, { status: 500 }); 
  }

  let body;
  try {
    // 2. Ambil raw body untuk verifikasi signature dan parsing
    body = await request.text();
    console.debug('Raw webhook body received (length):', body.length);
  } catch (err) {
    console.error('Failed to read request body:', err);
    return NextResponse.json({ error: 'Failed to read request body' }, { status: 400 });
  }

  try {
    // 3. Verifikasi signature menggunakan server key rahasia
    // --- PERBAIKAN UTAMA DI SINI ---
    if (!verifySignature(body, request.headers, serverKey)) {
      console.error('Webhook signature verification failed.');
      // Kembalikan 400 Bad Request jika signature tidak valid
      return NextResponse.json({ error: 'Invalid signature' }, { status: 400 }); 
    }
    console.log('Webhook signature verified successfully.');

    // 4. Parse notifikasi JSON
    let notification;
    try {
      notification = JSON.parse(body);
    } catch (parseError) {
      console.error('Failed to parse JSON notification body:', parseError);
      return NextResponse.json({ error: 'Invalid JSON in request body' }, { status: 400 });
    }

    // 5. Ekstrak informasi penting
    const orderId = notification.order_id;
    const transactionStatus = notification.transaction_status;
    const fraudStatus = notification.fraud_status;
    const paymentType = notification.payment_type;
    const grossAmount = notification.gross_amount;

    if (!orderId) {
       console.error('Missing order_id in notification');
       return NextResponse.json({ error: 'Missing order_id' }, { status: 400 });
    }

    console.log(`Processing notification for Order ID: ${orderId}`);
    console.log(` - Transaction Status: ${transactionStatus}`);
    console.log(` - Fraud Status: ${fraudStatus}`);
    console.log(` - Payment Type: ${paymentType}`);
    console.log(` - Gross Amount: ${grossAmount}`);

    // 6. Tangani status transaksi yang berbeda
    switch (transactionStatus) {
      case 'capture':
        if (fraudStatus === 'accept') {
          console.log(`Transaction ${orderId} captured and accepted.`);
          await updateUserSubscription(orderId, 'capture', notification);
          await sendConfirmationEmail(notification);
        } else if (fraudStatus === 'challenge') {
          console.log(`Transaction ${orderId} captured but challenged.`);
          await updateUserSubscription(orderId, 'challenge', notification);
          // Mungkin kirim notifikasi internal untuk review
        }
        break;

      case 'settlement':
        console.log(`Transaction ${orderId} settled.`);
        await updateUserSubscription(orderId, 'settlement', notification);
        await sendConfirmationEmail(notification);
        break;

      case 'pending':
        console.log(`Transaction ${orderId} is pending.`);
        await updateUserSubscription(orderId, 'pending', notification);
        // Mungkin kirim notifikasi bahwa pembayaran sedang diproses
        break;

      case 'deny':
        console.log(`Transaction ${orderId} was denied.`);
        await updateUserSubscription(orderId, 'deny', notification);
        // Mungkin kirim notifikasi ke pengguna
        break;

      case 'cancel':
        console.log(`Transaction ${orderId} was cancelled.`);
        await updateUserSubscription(orderId, 'cancel', notification);
        // Mungkin kirim notifikasi ke pengguna
        break;

      case 'expire':
        console.log(`Transaction ${orderId} has expired.`);
        await updateUserSubscription(orderId, 'expire', notification);
        // Mungkin kirim notifikasi ke pengguna
        break;

      default:
        console.log(`Unhandled transaction status '${transactionStatus}' for order ${orderId}`);
    }

    // 7. Kembalikan respons sukses ke Midtrans
    console.log(`Successfully processed notification for order ${orderId}`);
    return NextResponse.json({ received: true }); // Status 200 OK default

  } catch (error) {
    // Tangkap error yang tidak terduga
    console.error('Unexpected error in webhook processing:', error);
    // Kembalikan 500 untuk error server internal
    return NextResponse.json({ error: 'Internal server error during webhook processing' }, { status: 500 }); 
  }
}

// Handle unsupported HTTP methods
export function GET() {
  console.warn('GET request made to webhook endpoint');
  return NextResponse.json({ error: 'Method not allowed' }, { status: 405 });
}

export function OPTIONS() {
  // Tangani preflight CORS jika diperlukan (meskipun umumnya tidak untuk webhook)
  console.debug('OPTIONS request made to webhook endpoint');
  return new Response(null, { status: 204 });
}
