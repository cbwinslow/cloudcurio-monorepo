import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'

export default NextAuth({
  providers: [
    GitHub({
      // ...existing config...
    }),
  ],
  callbacks: {
    async signIn({ user }) {
      if (user.email === 'blaine.winslow@gmail.com') {
        user.role = 'admin'
      }
      return true
    },
    // ...existing callbacks...
  },
  // ...existing config...
})