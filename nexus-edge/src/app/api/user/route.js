export async function GET(request) {
  // Opsional: proteksi hanya untuk admin
  const session = await getServerSession(authOptions);
  if (!session || session.user.email !== "admin@example.com") {
    return new Response(JSON.stringify({ error: "Forbidden" }), {
      status: 403,
    });
  }

  const users = await prisma.user.findMany({
    select: {
      id: true,
      name: true,
      email: true,
      image: true,
      accounts: {
        where: { provider: "google" },
        select: { provider: true },
      },
    },
  });

  return new Response(JSON.stringify(users), { status: 200 });
}