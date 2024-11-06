import { logInfo, logError } from '@/lib/logger';
import { ErrorCode, fetchServer } from "@/lib/fetchServer";

export async function fetchEmail({ accessToken }: { accessToken: string }) {
  
  try {
    logInfo("Fetching email...");
    const res = await fetchServer("/me", {
      method: "GET",
      headers: {
        Cookie: `access_token=${accessToken}`,
      },
    });

    const result = await res.json();  

    if (res.ok) {
      logInfo(`Email fetched successfully: ${result.email}`);
      return result.email;
    } else if (res.status == 401) {
      throw new ErrorCode(result.detail, result.code);
    } else {
      logError(`Failed to load email: ${result.detail}`);
      return "Failed to load email";
    }
  } catch (error) {
    logError(error as Error);
    throw error;
  } 
}

export async function fetchFolders({ accessToken }: { accessToken: string }) {
  
  try {
    logInfo("Fetching folders...");
    const res = await fetchServer("/folders", {
      method: "GET",
      headers: {
        Cookie: `access_token=${accessToken}`,
      },
    });

    const result = await res.json();

    if (res.ok) {
      logInfo(`Folders fetched successfully: ${JSON.stringify(result.folders)}`);
      return result.folders;
    } else {
      logError(`Failed to fetch folders: ${result.detail}`); 
      throw new ErrorCode(result.detail, result.code);
    }
  } catch (error) {
    logError(error as Error);
    throw error;
  } 
}

export async function fetchNoFolderChatRooms({
  accessToken,
}: {
  accessToken: string;
}) {  
  try {
    logInfo("Fetching chat rooms with folderId=0...");
    const res = await fetchServer("/chatrooms?folderId=0", {
      method: "GET",
      headers: {
        Cookie: `access_token=${accessToken}`,
      },
    });

    const result = await res.json();

    if (res.ok) {
      logInfo(`Chat rooms fetched successfully: ${JSON.stringify(result.chat_rooms)}`); 
      return result.chat_rooms;
    } else {
      logError(`Failed to fetch chat rooms: ${result.detail}`); 
      throw new ErrorCode(result.detail, result.code);
    }
  } catch (error) {
    logError(error as Error);
    throw error;
  } 
}