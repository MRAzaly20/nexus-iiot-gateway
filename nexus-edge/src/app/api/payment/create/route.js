import { NextResponse } from 'next/server';
import Midtrans from 'midtrans-client';

let snap = new Midtrans.Snap({
  isProduction: process.env.MIDTRANS_IS_PRODUCTION === 'true',
  serverKey: process.env.MIDTRANS_SERVER_KEY,
  clientKey: process.env.NEXT_PUBLIC_MIDTRANS_CLIENT_KEY
});

export async function POST(request) {
  try {
    const { orderId, grossAmount, customerDetails, planId } = await request.json();

    // Validate input
    if (!orderId || !grossAmount || !customerDetails || !planId) {
      return NextResponse.json({ error: 'Missing required fields' }, { status: 400 });
    }
    console.log(customerDetails);
    // Prepare transaction parameters
    let parameter = {
      "transaction_details": {
        "order_id": orderId,
        "gross_amount": grossAmount
      },
      "customer_details": customerDetails,
      "item_details": [{
        "id": planId,
        "price": grossAmount,
        "quantity": 1,
        "name": `NexusEdge ${planId.charAt(0).toUpperCase() + planId.slice(1)} Plan`,
        "brand": "NexusEdge",
        "category": "IIoT Subscription"
      }],
      "callbacks": {
        "notification_url": "https://app.smtijogja.my.id/api/payment/webhook" 
      },
      "finish_redirect_url": "https://app.smtijogja.my.id/feature",
    };

    // Create transaction and get Snap token
    const token = await snap.createTransactionToken(parameter);
    //const { token } = transaction;

    return NextResponse.json({ token });

  } catch (error) {
    console.error('Payment creation error:', error);
    return NextResponse.json({ error: 'Failed to create payment' }, { status: 500 });
  }
}