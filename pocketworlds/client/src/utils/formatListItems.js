export const formatListItems = (text) => {
  const lines = text.split('\n').filter(line => line.trim());
  
  const listPatterns = [
    /^(\d+\.|\d+\)|\-|\*|•)\s+/,
  ];

  let isNumberedList = false;
  let isList = lines.some((line, i) => {
    if (/^\d+[\.\)]\s/.test(line.trim())) {
      isNumberedList = true;
      return true;
    }
    return listPatterns.some(pattern => pattern.test(line.trim()));
  });

  if (!isList) return text;

  const parts = lines.reduce((acc, line, i) => {
    if (i === 0 && !listPatterns[0].test(line)) {
      acc.intro = line;
    } else if (i === lines.length - 1 && !listPatterns[0].test(line)) {
      acc.outro = line;
    } else if (listPatterns[0].test(line)) {
      const content = line.replace(listPatterns[0], '').trim();
      acc.items.push(content);
    }
    return acc;
  }, { intro: '', items: [], outro: '' });

  return {
    intro: parts.intro,
    items: parts.items,
    outro: parts.outro,
    isNumberedList
  };
};