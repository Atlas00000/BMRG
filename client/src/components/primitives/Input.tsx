import type { InputHTMLAttributes } from 'react';
import './Input.css';

type Props = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
};

export function Input({ label, id, className = '', ...rest }: Props) {
  const inputId = id ?? rest.name;
  return (
    <label className={['ln-field', className].filter(Boolean).join(' ')} htmlFor={inputId}>
      {label ? <span className="ln-field__label">{label}</span> : null}
      <input id={inputId} className="ln-input" {...rest} />
    </label>
  );
}
