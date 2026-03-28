# Frontend - Clinic AI Receptionist

Welcome to the frontend folder! This is where your user-facing application will live.

## Setup Options

### React + TypeScript (Recommended)
```bash
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

### Next.js
```bash
npx create-next-app@latest .
npm run dev
```

### Vue
```bash
npm create vue@latest .
npm install
npm run dev
```

## Integration with Backend

The frontend should communicate with the backend API at:
- **Local**: `http://localhost:8000`
- **Production**: Your deployed backend URL

### Example API Call (JavaScript/TypeScript)

```typescript
async function sendMessage(message: string) {
  const response = await fetch('http://localhost:8000/api/v1/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });
  const data = await response.json();
  return data.response;
}
```

### Example API Call (React)

```typescript
import { useState } from 'react';

export function ChatWidget() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  async function handleSend() {
    const res = await fetch('/api/v1/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    setResponse(data.response);
  }

  return (
    <div>
      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={handleSend}>Send</button>
      {response && <p>{response}</p>}
    </div>
  );
}
```

## API Endpoints

**Chat (AI Agent)**
- `POST /api/v1/chat` - Send message to AI receptionist

**Appointments**
- `GET /api/v1/appointments` - List all appointments
- `GET /api/v1/appointments/{id}` - Get specific appointment
- `POST /api/v1/appointments` - Create new appointment
- `PUT /api/v1/appointments/{id}` - Update appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment

**Health**
- `GET /api/v1/health` - Check API status

See the backend's Swagger docs at `http://localhost:8000/docs` for detailed API specs.

## Environment Variables

Create a `.env` or `.env.local` file:

```
VITE_API_URL=http://localhost:8000
# or
REACT_APP_API_URL=http://localhost:8000
```

## Resources

- [Backend API Documentation](../README.md)
- [FastAPI Docs](http://localhost:8000/docs)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)

---

**Ready to build?** Start with your preferred framework above!
