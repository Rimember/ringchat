import { NextRequest, NextResponse } from 'next/server';
import { register, clsGauge, lcpGauge, ttfbGauge, fcpGauge, inpGauge } from '@/lib/metrics'; 

// POST 요청 처리 (Web Vitals 데이터를 수집)
export async function POST(request: NextRequest) {
  const body = await request.json(); // 요청의 본문 데이터 파싱

  // body.data가 존재하는지 확인
  if (!body.data || !Array.isArray(body.data)) {
    return NextResponse.json({ error: "Invalid data format" }, { status: 400 });
  }

  // Web Vitals 데이터를 처리하여 Prometheus 메트릭으로 변환
  body.data.forEach((metric) => {
    switch (metric.name) {
      case 'CLS':
        clsGauge.labels(metric.path, metric.id).set(metric.value);
        break;
      case 'LCP':
        lcpGauge.labels(metric.path, metric.id).set(metric.value);
        break;
      case 'TTFB':
        ttfbGauge.labels(metric.path, metric.id).set(metric.value);
        break;
      case 'FCP':
        fcpGauge.labels(metric.path, metric.id).set(metric.value);
        break;
      case 'INP':
        inpGauge.labels(metric.path, metric.id).set(metric.value);
        break;
      default:
        console.log(`Unknown metric type: ${metric.name}`);
    }
  });

  return NextResponse.json({ message: "Metrics POST request received" });
}

// GET 요청 처리 (수집된 메트릭을 Prometheus 텍스트 포맷으로 반환)
export async function GET(request: NextRequest) {
  const metrics = await register.metrics(); // 레지스트리에서 메트릭 가져오기
  return new Response(metrics, {
    headers: { 'Content-Type': register.contentType },
  });
}