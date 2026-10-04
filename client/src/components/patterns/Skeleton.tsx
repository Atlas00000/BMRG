import './Skeleton.css';

type Props = {
  width?: string | number;
  height?: string | number;
  className?: string;
};

export function Skeleton({ width = '100%', height = '0.75rem', className = '' }: Props) {
  return (
    <span
      className={['ln-skeleton-block', className].filter(Boolean).join(' ')}
      style={{ width, height }}
      aria-hidden
    />
  );
}

export function SkeletonMetricStrip() {
  return (
    <div className="ln-skeleton-strip" aria-busy="true" aria-label="Loading metrics">
      {Array.from({ length: 5 }).map((_, i) => (
        <div key={i} className="ln-skeleton-strip__cell">
          <Skeleton width="40%" height={10} />
          <Skeleton width={i === 0 ? '70%' : '55%'} height={i === 0 ? 28 : 22} />
        </div>
      ))}
    </div>
  );
}
