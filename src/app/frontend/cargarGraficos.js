//URL de donde se obtienen los datos
var urlBase = "http://172.25.0.3:8000/";


//Inicilizamos los array para los graficos
var arrMediaIncidentesClima = [];
var arrMediaPrecipitaciones = [];
var arrMediaTemperatura = [];
var arrMediaIncidentesPobreza = [];
var arrMediaPobreza = [];
var arrMediaIncidentesNoFinde = [];
var arrMediaIncidentesFinde = [];
var arrMediaIncidentesLeyes = [];
var arrMediaLeyes = [];

/****************************************************
 * Nombre: fncCargarGraficosClima                   *
 * Descripcion: devuelve los datos para los graficos*
 * relacionados con el clima                        *
 * **************************************************/
function fncCargarGraficosClima(strEstado, strAnio){
    strUrlFinal = urlBase+"incidents/climate/";
    if(strEstado != "" && strAnio != ""){
        strUrlFinal += "?state="+strEstado+"&year="+strAnio;
    }else if(strEstado != ""){
        strUrlFinal += "?state="+strEstado;
    }else if(strAnio != ""){
        strUrlFinal += "?year="+strAnio;
    }

    var sumByState = {};
    var countByState = {};

    $.ajax({
        url: strUrlFinal, // Ajusta la URL al puerto y ruta correctos
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            data.forEach(function(item){
                if (!sumByState[item.state]) {
                    sumByState[item.state] = {
                        n_incidents: 0,
                        average_precipitation: 0,
                        average_temperature: 0
                    };
                    countByState[item.state] = 0;
                }

                sumByState[item.state].n_incidents += item.n_incidents;
                sumByState[item.state].average_precipitation += item.average_precipitation;
                sumByState[item.state].average_temperature += item.average_temperature;
                countByState[item.state]++;
                });

            // Calcular la media por estado
            for (var state in sumByState) {
                if (sumByState.hasOwnProperty(state)) {
                    arrMediaIncidentesClima.push(sumByState[state].n_incidents / countByState[state]);
                    arrMediaPrecipitaciones.push(sumByState[state].average_precipitation / countByState[state]);
                    arrMediaTemperatura.push(sumByState[state].average_temperature / countByState[state]);
                }
            }
            fncPintarGraficoClima();
        },
        error: function (error) {
            console.error('Error en la llamada AJAX:', error);
        }
    });
}

/****************************************************
 * Nombre: fncCargarGraficosPobreza                 *
 * Descripcion: devuelve los datos para los graficos*
 * relacionados con la pobreza                      *
 * **************************************************/
function fncCargarGraficosPobreza(strEstado, strAnio){
    strUrlFinal = urlBase+"incidents/population_poverty/";
    if(strEstado != "" && strAnio != ""){
        strUrlFinal += "?state="+strEstado+"&year="+strAnio;
    }else if(strEstado != ""){
        strUrlFinal += "?state="+strEstado;
    }else if(strAnio != ""){
        strUrlFinal += "?year="+strAnio;
    }

    var sumByState2 = {};
    var countByState2 = {};

    $.ajax({
        url: strUrlFinal, // Ajusta la URL al puerto y ruta correctos
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            data.forEach(function(item){
            if (!sumByState2[item.state]) {
                sumByState2[item.state] = {
                    n_incidents: 0,
                    poverty_rate: 0,
                };
                countByState2[item.state] = 0;
            }

            sumByState2[item.state].n_incidents += item.n_incidents;
            sumByState2[item.state].poverty_rate += parseFloat(item.poverty_rate);
            countByState2[item.state]++;
            });
            
            // Calcular la media por estado
            for (var state in sumByState2) {
                if (sumByState2.hasOwnProperty(state)) {
                    arrMediaIncidentesPobreza.push(sumByState2[state].n_incidents / countByState2[state]);
                    arrMediaPobreza.push((sumByState2[state].poverty_rate / countByState2[state])*100);
                }
            }
            fncPintarGraficoPobreza();
        },
        error: function (error) {
            console.error('Error en la llamada AJAX:', error);
        }
    });
}

/****************************************************
 * Nombre: fncCargarGraficosFindes                  *
 * Descripcion: devuelve los datos para los graficos*
 * relacionados con el fin de semana                *
 * **************************************************/
function fncCargarGraficosFindes(strEstado, strAnio){
    strUrlFinal = urlBase+"incidents/weekend/";
    if(strEstado != "" && strAnio != ""){
        strUrlFinal += "?state="+strEstado+"&year="+strAnio;
    }else if(strEstado != ""){
        strUrlFinal += "?state="+strEstado;
    }else if(strAnio != ""){
        strUrlFinal += "?year="+strAnio;
    }

    var sumByState3 = {};
    var countByState3 = {};
    var sumByState3F = {};
    var countByState3F = {};

    $.ajax({
        url: strUrlFinal, // Ajusta la URL al puerto y ruta correctos
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            data.forEach(function(item){
                if(item.is_weekend){
                    if (!sumByState3F[item.state]) {
                        sumByState3F[item.state] = {
                            n_incidents: 0
                        };
                        countByState3F[item.state] = 0;
                    }
        
                    sumByState3F[item.state].n_incidents += parseFloat(item.n_incidents_per_day);
                    countByState3F[item.state]++;
                }else{
                    if (!sumByState3[item.state]) {
                        sumByState3[item.state] = {
                            n_incidents: 0
                        };
                        countByState3[item.state] = 0;
                    }
        
                    sumByState3[item.state].n_incidents += parseFloat(item.n_incidents_per_day);
                    countByState3[item.state]++;
                }

            });
            
            // Calcular la media por estado
            for (var state in sumByState3) {
                if (sumByState3.hasOwnProperty(state)) {
                    arrMediaIncidentesNoFinde.push(sumByState3[state].n_incidents / countByState3[state]);
                }
            }
            for (var state in sumByState3F) {
                if (sumByState3F.hasOwnProperty(state)) {
                    arrMediaIncidentesFinde.push(sumByState3F[state].n_incidents / countByState3F[state]);
                }
            }
            fncPintarGraficoFinde();
        },
        error: function (error) {
            console.error('Error en la llamada AJAX:', error);
        }
    });
}

/****************************************************
 * Nombre: fncCargarGraficosLeyes                   *
 * Descripcion: devuelve los datos para los graficos*
 * relacionados con las leyes                       *
 * **************************************************/
function fncCargarGraficosLeyes(strEstado, strAnio){
    strUrlFinal = urlBase+"incidents/firearm_laws/";
    if(strEstado != "" && strAnio != ""){
        strUrlFinal += "?state="+strEstado+"&year="+strAnio;
    }else if(strEstado != ""){
        strUrlFinal += "?state="+strEstado;
    }else if(strAnio != ""){
        strUrlFinal += "?year="+strAnio;
    }

    var sumByState4 = {};
    var countByState4 = {};
    $.ajax({
        url: strUrlFinal,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            data.forEach(function(item){
                if (!sumByState4[item.state]) {
                    sumByState4[item.state] = {
                        n_incidents: 0,
                        lawtotal: 0,
                    };
                    countByState4[item.state] = 0;
                }
    
                sumByState4[item.state].n_incidents += parseFloat(item.n_incidents);
                sumByState4[item.state].lawtotal += parseFloat(item.lawtotal);
                
                countByState4[item.state]++;
            });
            
            // Calcular la media por estado
            for (var state in sumByState4) {
                if (sumByState4.hasOwnProperty(state)) {
                    arrMediaIncidentesLeyes.push(sumByState4[state].n_incidents / countByState4[state]);
                    arrMediaLeyes.push(sumByState4[state].lawtotal / countByState4[state]);
                }
            }
            fncPintarGraficoLeyes();
        },
        error: function (error) {
            console.error('Error en la llamada AJAX:', error);
        }
    });
}

/****************************************************
 * Nombre: fncCargarGraficos                        *
 * Descripcion:                                     *
 * **************************************************/
function fncCargarGraficos(){
    fncCargando(true);
    strEstado = $("#cmbEstados").val();
    strAnio = $("#cmbAnio").val();

    fncCargarGraficosClima(strEstado, strAnio);
    fncCargarGraficosPobreza(strEstado, strAnio);
    fncCargarGraficosFindes(strEstado, strAnio);
    fncCargarGraficosLeyes(strEstado, strAnio);
}

/****************************************************
 * Nombre: fncPintarGraficoClima                    *
 * Descripcion: pinta el grafico segun el clima     *
 * **************************************************/
function fncPintarGraficoClima(){
    const ctx = document.getElementById('graficoClima');

    chartClima.destroy();

    chartClima = new Chart(ctx, {
        data: {
        labels: estados,
        datasets: [{
            type: 'bar',    
            label: 'Media de Precipitaciones',
            data: arrMediaPrecipitaciones,
            backgroundColor: ['rgb(97, 191, 255)'],
            borderWidth: 1,
            order: 3
        },{
            type: 'bar',
            label: 'Media de Temperatura',
            data: arrMediaTemperatura,
            backgroundColor: ['rgb(255, 209, 97)'],
            borderWidth: 1,
            order: 2
        },{
            type: 'line',
            label: 'Media de Incidentes Mensuales',
            data: arrMediaIncidentesClima,
            backgroundColor: ['rgb(240, 49, 31)'],
            borderWidth: 1,
            order: 1
        }]
        },
        options: {
        scales: {
            y: {
            beginAtZero: true
            }
        }
        }
    });
}

/****************************************************
 * Nombre: fncPintarGraficoPobreza                  *
 * Descripcion: pinta el grafico segun la pobreza   *
 * **************************************************/
function fncPintarGraficoPobreza(){
    const ctx = document.getElementById('graficoPobreza');

    chartPobreza.destroy();

    chartPobreza = new Chart(ctx, {
        data: {
        labels: estados,
        datasets: [{
            type: 'bar',    
            label: '% Medio de Tasa de Pobreza',
            data: arrMediaPobreza,
            backgroundColor: ['rgb(97, 191, 255)'],
            borderWidth: 1,
            order: 5
        },{
            type: 'line',
            label: 'Media de Incidentes Anuales',
            data: arrMediaIncidentesPobreza,
            backgroundColor: ['rgb(240, 49, 31)'],
            borderWidth: 1,
            order: 4
        }]
        },
        options: {
        scales: {
            y: {
            beginAtZero: true
            }
        }
        }
    });
}

/****************************************************
 * Nombre: fncPintarGraficoFinde                    *
 * Descripcion: pinta el grafico segun los findes   *
 * **************************************************/
function fncPintarGraficoFinde(){
    const ctx = document.getElementById('graficoFindes');

    chartFinde.destroy();

    chartFinde = new Chart(ctx, {
        data: {
        labels: estados,
        datasets: [{
            type: 'bar',    
            label: 'Media de Incidentes Fin de Semana',
            data: arrMediaIncidentesFinde,
            backgroundColor: ['rgb(97, 191, 255)'],
            borderWidth: 1
        },{
            type: 'bar',
            label: 'Media de Incidentes Día de Diario',
            data: arrMediaIncidentesNoFinde,
            backgroundColor: ['rgb(240, 49, 31)'],
            borderWidth: 1
        }]
        },
        options: {
        scales: {
            y: {
            beginAtZero: true
            }
        }
        }
    });
}

/****************************************************
 * Nombre: fncPintarGraficoLeyes                    *
 * Descripcion: pinta el grafico segun las leyes    *
 * **************************************************/
function fncPintarGraficoLeyes(){
    const ctx = document.getElementById('graficoLeyes');

    chartLeyes.destroy();

    chartLeyes = new Chart(ctx, {
        data: {
        labels: estados,
        datasets: [{
            type: 'bar',    
            label: 'Media de Incidentes Anuales',
            data: arrMediaIncidentesLeyes,
            backgroundColor: ['rgb(97, 191, 255)'],
            borderWidth: 1
        },{
            type: 'bar',
            label: 'Media de Leyes de Regulación de Armas',
            data: arrMediaLeyes,
            backgroundColor: ['rgb(240, 49, 31)'],
            borderWidth: 1
        }]
        },
        options: {
        scales: {
            y: {
            beginAtZero: true
            }
        }
        }
    });
    fncCargando(false);
}