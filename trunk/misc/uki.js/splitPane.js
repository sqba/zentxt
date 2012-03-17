/**
@example_title Split pane
@example_order 31
@example_html
    <style>body, html { overflow: hidden; margin: 0; padding: 0; }</style>
    <script src="/src/uki.cjs"></script>
    <script src="splitPane.js"></script>
*/

// custom formatter for duration column
function formatTime (t) {
    var m = Math.floor(t/60/1000),
        s = Math.floor(t/1000 - m * 60);
        
    return m + ':' + (s > 9 ? s : '0' + s);
}

// formatter for highlighted strings
var hlt = '';
function formatHlted (t) {
    return t;
    return hlt ? (t || '').replace(hlt, '<strong>' + hlt + '</strong>') : t;
}



// pregenerate list data (30000k items)
var data = ['this is', '30000k long', 'list'];
for (var i=3; i < 30000; i++) {
    data[i] = 'item #' + (i+1);
};




uki(
{   // create a split pane...
    view: 'HSplitPane', rect: '1000 600', anchors: 'left top right bottom',
    handlePosition: 200, leftMin: 1, rightMin: 300,
    // left part
    leftChildViews: [{
        view: 'ScrollPane', rect: '200 600', anchors: 'top left right bottom',
            childViews: { view: 'Box', rect: '0 0 200 900002', anchors: 'top left right', background: '#CCC',
                childViews: { view: 'List', rect: '0 0 200 900000', anchors: 'top left right', 
                    rowHeight: 30, id: 'filelist', throttle: 0, multiselect: false, textSelectable: false }
            }
    }],
    // right part
    rightChildViews: [{
        view: 'VSplitPane', rect: '1000 600', anchors: 'left top right bottom', vertical: true, handlePosition: 800, bottomMin: 1,
        // top part
        topChildViews: {
            view: 'MultilineTextField', rect: '790 490', anchors: 'top left right bottom'
        },
        // bottom part
        bottomChildViews: {
            view: 'Table', id: 'history', rect: '790 100', anchors: 'left top right bottom', columns: [
                { view: 'table.CustomColumn', label: 'Name', resizable: true, minWidth: 100, width: 250, formatter: formatHlted },
                { view: 'table.NumberColumn', label: 'Time', resizable: true, width: 50, formatter: formatTime },
                { view: 'table.CustomColumn', label: 'Artist', resizable: true, minWidth: 100, width: 150, formatter: formatHlted },
                { view: 'table.CustomColumn', label: 'Album', resizable: true, minWidth: 100, width: 150, formatter: formatHlted },
                { view: 'table.CustomColumn', label: 'Genre', resizable: true, width: 100 },
                { view: 'table.NumberColumn', label: 'Rating', resizable: true, width: 30 },
                { view: 'table.NumberColumn', label: 'Play Count', resizable: true, width: 30 }
            ], multiselect: true, textSelectable: false, style: {fontSize: '11px'}
        }
    }]
}).attachTo( window, '1000 600' );



// searchable model
window.DummyModel = uki.newClass(Searchable, new function() {
    this.init = function(data) {
        this.items = uki.map(data, function(row) {
            row = row.slice(1);
            row.searchIndex = row[0].toLowerCase();
            // var tmp = row[2];
            // row[2] = row[3];
            // row[3] = tmp;
            return row;
        })
    };
    
    this.matchRow = function(row, iterator) {
        return row.searchIndex.indexOf(iterator.query) > -1;
    };
});



// dinamicly load library json
window.onLibraryLoad = function(data) {
    uki('#loading').visible(false);
    var model = new DummyModel(data),
        lastQuery = '',
        table = uki('#history');
        
    model.bind('search.foundInChunk', function(chunk) {
        table.data(table.data().concat(chunk)).layout();
    });
        
    table.data(model.items).layout();
    
    uki('TextField').bind('keyup click', function() {
        if (this.value().toLowerCase() == lastQuery) return;
        lastQuery = this.value().toLowerCase();
        if (lastQuery.match(/\S/)) {
            hlt = lastQuery;
            table.data([]);
            model.search(lastQuery);
        } else {
            hlt = '';
            table.data(model.items);
        }
    });
    document.body.className += '';
   
};
var script = document.createElement('script'),
    head = document.getElementsByTagName('head')[0];
script.src = 'library.js';
head.insertBefore(script, head.firstChild);


uki('#filelist').data(data);
//uki('#filelist').render();

uki('#filelist').bind('click', function(e) {
    var item = this.data()[this.selectedIndex()];
    uki('MultilineTextField').value(item);
}).parent();

uki('#history').bind('click', function(e) {
    var item = this.data()[this.selectedIndex()][0];
    uki('MultilineTextField').value(item);
}).parent();


/*
// on slider change update text field
uki('HSplitPane Slider').bind('change', function() {
    uki('TextField').value(this.value())
});

// on button click clear the text field
uki('Button[text~="Clear"]').bind('click', function() {
    uki('#field').value('') // find by id
}).parent();
*/


