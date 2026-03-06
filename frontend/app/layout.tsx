export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body style={{
        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#0f1117',
        color: '#ffffff',
        margin: 0,
        padding: 0,
      }}>
        {children}
      </body>
    </html>
  )
}