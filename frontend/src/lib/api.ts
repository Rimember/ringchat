import { ErrorCode, fetchServer } from "@/lib/fetch";

interface fetchProps {
  domain: string;
  accessToken: string;
}

export async function fetchEmail(props: fetchProps) {
  try {
    const res = await fetchServer(props.domain, "/me", {
      method: "GET",
      headers: {
        Cookie: `access_token=${props.accessToken}`,
      },
    });

    const result = await res.json();
    if (res.ok) {
      return result.email;
    } else if (res.status == 401) {
      throw new ErrorCode(result.detail, result.code);
    } else {
      return "Failed to load email";
    }
  } catch (error) {
    console.log("Error occurred while fetching email.");
    throw error;
  }
}

export async function fetchFolders(props: fetchProps) {
  try {
    const res = await fetchServer(props.domain, "/folders", {
      method: "GET",
      headers: {
        Cookie: `access_token=${props.accessToken}`,
      },
    });

    const result = await res.json();
    if (res.ok) {
      return result.folders;
    } else {
      throw new ErrorCode(result.detail, result.code);
    }
  } catch (error) {
    console.log("Error occurred while fetching folders.");
    throw error;
  }
}

export async function fetchNoFolderChatRooms(props: fetchProps) {
  try {
    const res = await fetchServer(props.domain, "/chatrooms?folderId=0", {
      method: "GET",
      headers: {
        Cookie: `access_token=${props.accessToken}`,
      },
    });

    const result = await res.json();
    if (res.ok) {
      return result.chat_rooms;
    } else {
      throw new ErrorCode(result.detail, result.code);
    }
  } catch (error) {
    console.log("Error occurred while fetching chat rooms.");
    throw error;
  }
}
