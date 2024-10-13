export class ErrorCode extends Error {
  code: string | undefined;

  constructor(message?: string | undefined, code?: string | undefined) {
    super(message);
    this.code = code;
  }
}

export async function fetchClient(path: string, options: RequestInit = {}) {
  const url = `${process.env.NEXT_PUBLIC_API_URL}${path}`;
  console.log(url)
  console.log(`${process.env.NEXT_PUBLIC_API_URL}`)

  const headers = new Headers({
    ...options.headers,
    "Content-Type": "application/json",
  });

  try {
    const res = await fetch(url, {
      ...options,
      headers,
      credentials: "include",
    });
    return res;
  } catch (error) {
    throw error;
  }
}

export async function fetchServer(path: string, options: RequestInit = {}) {
  const url = `${process.env.NEXT_PUBLIC_SERVER_API_URL}${path}`;

  const headers = new Headers({
    ...options.headers,
    "Content-Type": "application/json",
  });

  try {
    const res = await fetch(url, {
      ...options,
      headers,
      credentials: "include",
    });
    return res;
  } catch (error) {
    throw error;
  }
}
