//<script>

function Dialogv69b9295d4cad7() {
	var me = this;
	me.id = "dialogv69b9295d4cad7";
	me.GetElement = function () { return document.getElementById( me.id ); };
	me.GetEventHandlerName = function () { return "dialoghandlerv69b9295d4cad7"; };

	this.dialog_controls = [
		new DialogInput("inputDate", this, 0,new ElementAccessorDate(65)),
		new DialogInput("declination", this, 0,new ElementAccessorOutput()),
		new DialogInput("lat", this, new ValidatorRange( -90, 90),new ElementAccessorCoordinate()),
		new DialogInput("hmax", this, 0,new ElementAccessorOutput()),
		new DialogInput("calculate", this, 0,new ElementAccessorOperation()),
		new DialogInput("_progress_", this, 0,new ElementAccessorDefault()),
		new DialogInput("", this, 0,new ElementAccessorDefault())
	];

	me.dialog_controls._all ={};
	me.dialog_controls.forEach( function( e ) { 
		if (me[e.id]===undefined) me[e.id] = e; 
		me.dialog_controls._all[e.id] = e;} 
    );
	this.addHandler = function ( handler ) {
        this.dialog_controls.forEach(function(c) { c.addHandler( handler);});
	};
    this.SetValues = function ( values ) {
        this.dialog_controls.forEach(function(c) {
            if ( values[c.id]!==undefined ) { c.SetValue( values[c.id] ); }});
    };
    this.Clear = function ( ) {
        this.dialog_controls.forEach(function( c) { c.ResetValue();});
    };
    this.SetDefaultValues = function () { this.Clear();};
    this.GetValues = function () {var ret = {}; 
        this.dialog_controls.forEach(function( c) { ret[c.id] = c.GetValue();});
        return ret;
    };
    this.Validate = function ( ) {
        for(var i=0;i<me.dialog_controls.length;++i) if (!me.dialog_controls[i].Validate()) return false; 
        return true;
    };
    this.layout = function ( ) {}
};

document.addEventListener("DOMContentLoaded", function(event) {
    var dlg = new Dialogv69b9295d4cad7();
    var hd = new CalculatorHandler(new function () {
        var me = this;
        me.id = 10485;
        me.global = 1;
        var outputs = {};
        me.sinks={change:[],done:[]};
        me.startOnLoad = 1;
        me.infinite = 0;
        var inputs = {};
        var renderers = {};
        var recordsets = {};
        var diagrams = {};
        var handler, dialog, refreshTimer;
        var outer = this;
        me.adapter = { encoder:{"inputDate":Date2String},decoder:{"inputDate":String2Date}};
        me.timeout = 1500;
        me.auto = 1;
        me.init = function ( h, dlg ) { 
            var o; handler=h;dialog =dlg;
            me.control = new CalcController(h,me.id);
            var n; var fn;n='inputDate';
            if ( dlg[n] ) { inputs[n] = dlg[n]; }n='lat';
            if ( dlg[n] ) { inputs[n] = dlg[n]; }o = dlg.declination;outputs[o.id] =o;
            o.formatter =new FormatterDegrees(0);
            o = dlg.hmax;
            outputs[o.id] =o;
            o.formatter =new FormatterDegrees(0);
            handler.onReady();};
        me.stop = function() {};
        me.start = function() {
            handler.onStart();
            var inputValues = me.getInputValues();me.control.onCalculate( inputValues );
        };
        me.getInputs = function() {
            return inputs;
        };
        function objectValues( a, o ) {
            for(var n in o) {
                a.push( o[n] );
            }
        }
        me.getOutputs = function() {
            var ret = [];
            objectValues( ret, outputs );
            objectValues( ret, diagrams );
            objectValues( ret, renderers );
            return ret;
        };
        me.getInputValues = function() {
            var r = {};
            for( var n in inputs) {
                r[n] = inputs[n].GetValue();
            }
            return r;
        };
        me.setResult = function( res, done ) {
            outputs.declination.SetValue(res.declination);
            outputs.hmax.SetValue(res.hmax);
            if (done) { 
                handler.onStop();
                if ( PCF.requestFormulaUpdate( false ) ) { 
                    var mjx = window.MathJax; 
                    mjx.Hub.Queue(["Typeset",mjx.Hub]);
                };
            }
        }
    },
    {calculate:"Calculer", stop:"Arrêt"});;
    hd.initdialog(dlg);
    dlg.addHandler(hd);
    window.dialoghandlerv69b9295d4cad7 = hd;
}
);

//</script>