import { Text } from '../primitives';
import './EmptyState.css';

type Props = {
  title: string;
  detail: string;
};

/** Copy-only empty — no illustration / emoji. */
export function EmptyState({ title, detail }: Props) {
  return (
    <div className="ln-empty" role="status">
      <Text as="div" variant="label" tone="faint">
        Empty
      </Text>
      <Text as="h2" variant="title">
        {title}
      </Text>
      <Text as="p" tone="muted">
        {detail}
      </Text>
    </div>
  );
}
