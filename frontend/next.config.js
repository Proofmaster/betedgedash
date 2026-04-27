/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  // Disable image optimization since we aren't using images yet, 
  // which prevents build errors during static export.
  images: { unoptimized: true } 
}

module.exports = nextConfig
