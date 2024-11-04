import fs from 'fs';
import path from 'path';

// 로그 디렉토리 설정
const logDir = path.join(process.cwd(), 'logs');

// 로그 파일 이름 생성 함수
function getLogFileName(): string {
  const today = new Date();
  const dateString = today.toISOString().split('T')[0];
  return path.join(logDir, `${dateString}.log`);
}

// 로그 스트림 생성
let logStream = createLogStream();

// 로그 스트림 생성 함수
function createLogStream() {
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir); // 로그 디렉토리 없으면 생성
  }
  return fs.createWriteStream(getLogFileName(), { flags: 'a' });
}

// 에러 로깅 함수
export function logError(error: Error): void {
  const errorMsg = `[ERROR] - ${error.message}\n`;
  logStream.write(errorMsg);
  console.error(error);
}

// 정보 로깅 함수 (필요에 따라 추가 가능)
export function logInfo(message: string): void {
  const infoMsg = `[INFO] - ${message}\n`;
  logStream.write(infoMsg);
  console.info(message);
}

// 주기적으로 로그 스트림을 새로 고침하여 날짜 변경 확인
setInterval(() => {
  const currentLogFile = getLogFileName();
  if (!logStream.path.endsWith(currentLogFile)) {
    logStream.end(); // 현재 스트림 종료
    logStream = createLogStream(); // 새 스트림 생성
  }
}, 60 * 1000); // 매 1분마다 확인
