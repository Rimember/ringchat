import { Gauge, Registry } from 'prom-client';

// Prometheus 레지스트리 생성
const register = new Registry();

// Web Vitals 메트릭을 위한 게이지 생성
const clsGauge = new Gauge({
  name: 'web_vitals_cls',
  help: 'Cumulative Layout Shift',
  labelNames: ['path', 'id'],
  registers: [register],
});

const lcpGauge = new Gauge({
  name: 'web_vitals_lcp',
  help: 'Largest Contentful Paint',
  labelNames: ['path', 'id'],
  registers: [register],
});

const ttfbGauge = new Gauge({
  name: 'web_vitals_ttfb',
  help: 'Time to First Byte',
  labelNames: ['path', 'id'],
  registers: [register],
});

const fcpGauge = new Gauge({
  name: 'web_vitals_fcp',
  help: 'First Contentful Paint',
  labelNames: ['path', 'id'],
  registers: [register],
});

const inpGauge = new Gauge({
  name: 'web_vitals_inp',
  help: 'Interaction to Next Paint',
  labelNames: ['path', 'id'],
  registers: [register],
});

// 레지스트리와 게이지들을 export하여 다른 곳에서 사용 가능하게 함
export { register, clsGauge, lcpGauge, ttfbGauge, fcpGauge, inpGauge };