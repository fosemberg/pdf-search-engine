import React, { useRef, useState, useEffect } from 'react';
import Editor from 'react-simple-code-editor';
import { useField } from '@unform/core';

import { highlight, languages } from 'prismjs';

import 'prismjs/components/prism-markup';
import 'prismjs/components/prism-css';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-sql';
import 'prismjs/themes/prism-dark.css';

interface Props {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}

const InputWithSqlHighlight: React.FC<Props> = (
  {
    value,
    onChange,
    placeholder,
  }
) => {
  const editorRef = useRef(null);

  return (
    <Editor
      className="editor form-control"
      textareaId={'id'}
      value={value}
      defaultValue={''}
      onValueChange={onChange}
      highlight={code => highlight(code, languages.sql, 'sql')}
      padding={6}
      ref={editorRef}
      textareaClassName={'form-control'}
      placeholder={placeholder}
    />
  );
};

export default InputWithSqlHighlight;
