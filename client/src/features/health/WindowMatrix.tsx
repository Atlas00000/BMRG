import type { WindowHealthDto, WindowId } from '../../../api/adapters/artefacts';
import { Badge, Text } from '../../components/primitives';
import './WindowMatrix.css';

type Props = {
  windows: WindowHealthDto[];
  selected: WindowId;
  onSelect: (id: WindowId) => void;
  magic: number | null;
};

export function WindowMatrix({ windows, selected, onSelect, magic }: Props) {
  return (
    <div className="ln-window-matrix">
      <div className="ln-window-matrix__head">
        <Text as="div" variant="label" tone="faint">
          Window matrix
        </Text>
        <Badge tone="signal">magic {magic ?? '—'}</Badge>
      </div>
      <div className="ln-window-matrix__tabs" role="tablist" aria-label="Score windows">
        {windows.map((w) => {
          const active = w.id === selected;
          return (
            <button
              key={w.id}
              type="button"
              role="tab"
              aria-selected={active}
              className={['ln-window-matrix__tab', active ? 'is-active' : '', !w.available ? 'is-muted' : '']
                .filter(Boolean)
                .join(' ')}
              onClick={() => onSelect(w.id)}
            >
              <span className="ln-window-matrix__tab-label">{w.label}</span>
              <span className="ln-window-matrix__tab-meta">
                {w.available
                  ? `${w.start ?? '…'} → ${w.end ?? '…'}`
                  : 'no artefact'}
              </span>
              {!w.available ? (
                <Badge tone="neutral">queued</Badge>
              ) : (
                <Badge tone={active ? 'signal' : 'neutral'}>n {w.health.n}</Badge>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
