import React from 'react';
import { LANGUAGES } from '../../utils/constants';
import { Dropdown } from '../common/Dropdown';

interface LanguageSelectorProps {
  value: string;
  onChange: (languageCode: string) => void;
  label?: string;
  showFlag?: boolean;
}

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  value,
  onChange,
  label = 'Language',
  showFlag = true
}) => {
  const languageOptions = LANGUAGES.map(lang => ({
    value: lang.code,
    label: showFlag ? `${lang.flag} ${lang.name}` : lang.name
  }));

  const selectedLanguage = LANGUAGES.find(lang => lang.code === value);

  return (
    <div>
      {label && (
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        <Dropdown
          options={languageOptions}
          value={value}
          onChange={onChange}
        />
        {showFlag && selectedLanguage && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 pointer-events-none text-xl">
            {selectedLanguage.flag}
          </div>
        )}
      </div>
    </div>
  );
};
