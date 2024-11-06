"use client"; // 클라이언트 컴포넌트로 선언

import { useEffect } from 'react';
import { Metric, onCLS, onLCP, onTTFB, onFCP, onINP } from 'web-vitals';

export default function WebVitalsClient() {
  
  useEffect(() => {
    // Web Vitals 메트릭을 수집하고 서버로 전송
    function sendToAnalytics(metric: Metric) { 
      const body = JSON.stringify({
        data: [ // 'data' 필드 안에 배열로 감싸서 전송
          {
            name: metric.name,
            value: metric.value,
            id: metric.id,
            delta: metric.delta,
            path: window.location.pathname,
          }
        ]
      });

      // 데이터 전송 - navigator.sendBeacon()을 사용하거나 fetch()로 대체 가능
      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/metrics', body);
      } else {
        fetch('/api/metrics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body,
        }).catch((err) => console.error('Failed to send web vitals', err));
      }
    }

    // Web Vitals 메트릭 수집
    onCLS(sendToAnalytics);   // CLS 측정
    onLCP(sendToAnalytics);   // LCP 측정
    onTTFB(sendToAnalytics);  // TTFB 측정
    onFCP(sendToAnalytics);   // FCP 측정
    onINP(sendToAnalytics);   // INP 측정
  }, []);

  return null; // 렌더링할 UI는 없으므로 null 반환
}