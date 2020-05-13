function! oxfdictionary#add_highlight()
	syntax region DictionaryName start='\%1l' end='$'
	syntax region DictionaryCategory start='^[^-]\%>1l' end='$'
	highlight default link DictionaryCategory Number
	highlight default link DictionaryName Type
endfunction

function! oxfdictionary#show_floatingwindow(deflist, width, height, col, row, anchor)
	let buf = nvim_create_buf(v:false, v:true)
	call nvim_buf_set_lines(buf, 0, -1, v:true, a:deflist)
	let opts = {'relative': 'editor',
				\'width': a:width,
				\'height': a:height,
				\'col': a:col,
				\'row': a:row,
				\'anchor':a:anchor,
				\'style': 'minimal'
				\}
	let win = nvim_open_win(buf, 1, opts)
	call oxfdictionary#add_highlight()
endfunction
