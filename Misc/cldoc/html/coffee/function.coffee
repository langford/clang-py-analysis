class cldoc.Function extends cldoc.Node
    @title = ['Function', 'Functions']

    constructor: (@node) ->
        super(@node)

    render: ->
        e = cldoc.html_escape

        ret = '<div class="function">'
        ret += '<div class="declaration" id="' + e(@id) + '">'

        isvirt = @node.attr('virtual')
        isprot = @node.attr('access') == 'protected'
        isstat = @node.attr('static')

        if isvirt || isprot || isstat
            ret += '<ul class="specifiers">'

            if isstat
                ret += '<li class="static">static</li>'

            if isprot
                ret += '<li class="protected">protected</li>'

            if isvirt
                isover = @node.attr('override')

                if isover
                    ret += '<li class="override">override</li>'
                else
                    ret += '<li class="virtual">virtual</li>'

                if @node.attr('abstract')
                    ret += '<li class="abstract">abstract</li>'

            ret += '</ul>'

        # Return type
        retu = @node.children('return')
        returntype = null

        if retu.length > 0
            returntype = new cldoc.Type(retu.children('type'))
            ret += '<div class="return_type">' + returntype.render() + '</div>'

        ret += '<table class="declaration">'
        ret += '<tr><td class="identifier">' + e(@name) + '</td>'
        ret += '<td class="open_paren">(</td>'

        args = @node.children('argument')

        argtable = '<table class="arguments">'

        for i in [0..(args.length - 1)] by 1
            if i != 0
                ret += '</tr><tr><td colspan="2"></td>'

            arg = $(args[i])

            argtype = new cldoc.Type(arg.children('type'))
            ret += '<td class="argument_type">' + argtype.render() + '</td>'

            name = arg.attr('name')

            if i != args.length - 1
                name += ','

            ret += '<td class="argument_name">' + e(name) + '</td>'

            argtable += '<tr id="' + e(arg.attr('id')) + '">'
            argtable += '<td>' + e(arg.attr('name')) + '</td>'
            argtable += '<td>' + cldoc.Doc.either(arg)

            if argtype.allow_none
                argtable += '<span class="annotation">(may be <code>NULL</code>)</span>'

            argtable += '</td></tr>'

        if returntype and returntype.node.attr('name') != 'void'
            argtable += '<tr class="return">'
            argtable += '<td class="keyword">return</td>'
            argtable += '<td>' + cldoc.Doc.either(retu)

            if returntype.transfer_ownership == 'full'
                argtable += '<span class="annotation">(owned by caller)</span>'
            else if returntype.transfer_ownership == 'container'
                argtable += '<span class="annotation">(container owned by caller)</span>'

            argtable += '</tr>'

        if args.length == 0
            ret += '<td colspan="2"></td>'

        ret += '<td class="close_paren">)</td></tr></table></div>'
        ret += cldoc.Doc.either(@node)
        ret += argtable + '</table>'

        override = @node.children('override')

        if override.length > 0
            ret += '<div class="overrides"><span class="title">Overrides: </span>'

            for i in [0..override.length-1]
                ov = $(override[i])

                if i != 0
                    if i == override.length - 1
                        ret += ' and '
                    else
                        ret += ', '

                ret += cldoc.Page.make_link(ov.attr('ref'), ov.attr('name'))

        return ret + '</div>'

cldoc.Node.types.function = cldoc.Function

# vi:ts=4:et
