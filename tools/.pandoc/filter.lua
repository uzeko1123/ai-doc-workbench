function Table(el)
  if not el.attr.attributes['custom-style'] then
    el.attr.attributes['custom-style'] = 'Pandoc'
  end
  return el
end
