export default [
  {
    input: './lib/index.js',
    output: [
      {
        dir: 'dist',
        format: 'cjs',
        preserveModules: true
      }
    ],
    external: ['base64url']
  }
];
