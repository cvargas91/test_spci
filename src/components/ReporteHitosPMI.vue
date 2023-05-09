<template>
    <!--<q-card 
        class="my-card" 
        align="center"
    >-->
    <strong style="text-align:center; color:#385280; font-size:12pt; padding-top:85pt">
        Actividades:
    </strong>   
    
    <div class="row" style="background-color:#fcefd5;width:570pt; margin-right:0pt; margin-left:0pt; min-height:23pt; margin-bottom:0pt;margin-top:6pt:padding-top:0%; padding-right:40pt">
        <q-item-section style="margin-right:3pt">
            <q-item-label class="text-textoAzul">
                <p style="color:#385280; font-size:10pt; padding-top:5pt;padding-bottom:3pt; text-align:left; padding-left:45pt">
                    <b>{{idTactica}} | {{descripcionTactica}}</b>
                </p>
            </q-item-label>
        </q-item-section>
            <q-separator vertical/>
            <div class="flex-bottom col-2 q-px-lg text-textoAzul">
                <ManejoPlazo 
                    :hito="hitos[pasoHito]"
                />
            </div>
    </div>
    <q-card-actions align="around" style="padding-bottom:0pt">
        <p style="">
            <strong style="text-align:center; color:#385280; font-size:10pt">
                MdV
            </strong>   
        </p>

        <p>
            <strong style="text-align:center; color:#385280; font-size:10pt; align-right">
                Justificación por contingencia
            </strong>  
        </p>
    </q-card-actions>
    <q-card-section horizontal style="width:102%;height:10pt  padding-top:0pt" v-model="model">
        <q-card-section class="col 5" style="background-color:#d9e2f3">
            <q-expansion-item
                        expand-icon-toggle
                        expand-separator
                        label="Detalle MdV"
                        :caption="identificador"
                        class="text-btnAdjuntar"
                    >
                    <div v-for="(hitoEnReporte) in mdvs" :key="hitoEnReporte.id" style="word-wrap:break-word" >
                        <p style="text-align:left; padding-left:4pt"> * {{hitoEnReporte.label}}</p>
                    </div>
            </q-expansion-item>
        </q-card-section>
        <q-card-section>

        </q-card-section>
        <q-card-section class="col 5" style="background-color:#d9e2f3">
            <q-select
                v-model="justificacion" 
                :options="opcionesJustificacion"
                label="SI/NO" 
                style="width: 100%;"
            />
        </q-card-section>
    </q-card-section>

    <q-card-actions align="around" style="padding-bottom:0pt">
        
            <strong style="text-align:center; color:#385280; font-size:10pt">
                Nombre documento de <br/>justificación por contingencia
            </strong>   
        
            <strong style="text-align:center; color:#385280; font-size:10pt; align-right">
                Fecha entrega reporte
            </strong>  
        
    </q-card-actions>

    <q-card-section horizontal style="width:102%; padding-top:0pt">
        <div style="background-color:#d9e2f3; width:48%; margin-left:0pt; min-height:5pt; margin-right:0pt">
            <q-input
                v-model="reporteJustificacion"
                autogrow
                type="textarea"
                class="text-btnAdjuntar"
                style="margin-left:8pt"
                dense
            />  
        </div>
        
        <div style="background-color:#d9e2f3;width:48%;min-height:5pt;margin-left:28pt">
            <p style="text-align:center; color:#385280; font-size:10pt;padding-top:10pt;">
                {{fechaFormateada}}
            </p>   
        </div>
    </q-card-section>

    <strong style="text-align:center; color:#385280; font-size:10pt; margin-top:85pt">
        Comentarios al cumplimiento: 
    </strong>   
    <div style="background-color:#d9e2f3;width:102%; margin-right:0pt; margin-left:0pt;height:auto; margin-bottom:0pt;margin-top:0pt:padding-top:0%; padding-right:40pt">
        <q-input
            v-model="comentario_cumplimiento"
            borderless
            type="textarea"
            label="Ingresar comentario al cumplimiento"
            
        />
    </div>

        
    <div class="row justify-end q-gutter-sm q-ma-md" style="margin-right:0pt">
        
        <BotonCancelarReporte 
            opcion="hito"
            @guardarAvance="guardarAvance"
        />

        <q-btn
            v-if="validaPasoAtras()"
            color="btnVolver"
            @click="cambioAtras"
            label=" Hito Anterior  "
            class="q-ml-sm"
        />
        <q-btn
            v-if="validaPasoAdelante()"
            color="btnContinuar"
            @click="cambioAdelante"
            label="   Siguiente Hito   "
            class="q-ml-sm"
        />
        <q-btn
            v-if="!validaPasoAdelante()"
            color="btnContinuar"
            @click="avanzaReporte"
            label="   Siguiente   "
            class="q-ml-sm"
        />
    </div>  
    <br/>
    <br/>

    <br/>   
    <br/>
    <br/>
    
    <q-space />
    <br/>
</template>
<script>
    import { ref,toRef, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";
    import ManejoPlazo from "src/components/ManejoPlazo.vue";

    export default defineComponent({        
        components:{
            BotonCancelarReporte,
            ManejoPlazo,
        },
        props: {
            identificador: String,
            mdvs: Array,
            hitos: Array,
            reporteAccion: Object,
            fechaFormateada: String,
            funciones: Array,
        },
        watch: {        
            reporteAccion: async function (newValue, oldValue) {                
                this.pasoHito = 0;

                if(newValue.reporte_hitos.length){
                    this.comentario_cumplimiento = newValue.reporte_hitos[0].comentario_cumplimiento;
                }else{
                    this.comentario_cumplimiento = "";
                }

            },
            mdvs: function (newValue, oldValue) {
                this.mdvs = newValue;
                //this.descripcionTactica = this.mdvs[0].label;
            },
            hitos: function (newValue, oldValue) {
                this.hitos = newValue;
                this.descripcionTactica = this.hitos[0].label;
            },
        },
        setup(props) {  

            const store = useStore();
            const router = useRouter();
            const porcentaje = ref("");
            const nuevoReporte = computed(() => store.state.reporte);
            
            const acciones = computed(() => store.state.accion);
            const hitosIngresados = acciones.value.detalleAccion.hitos;
        
            const indicadorLogro = ref("");
            const opcionesJustificacion = ['Si','No'];
            const reporteJustificacion = ref("");
            const justificacion = ref("");

            const detalleProductos = computed(() => store.state.producto.totalHitos);

            const comentario_cumplimiento = ref('');
            const identificador = ref(props.identificador);

            const mdvs = ref(props.mdvs);
            const hitos = ref(props.hitos);
            const descripcionTactica = ref(hitos.value[0].label);
            
            const pasoHito =  ref(0);
            const arrayIdMDVReporte = ref('');
            const calculoAvance = () => {
                const detalle = {
                    idHito: hitos.value[pasoHito.value].value,
                    detalleProductos: detalleProductos.value
                };
                
                store.dispatch("accion/reqDetalleHitosAReporte", detalle);
                arrayIdMDVReporte.value = acciones.value.mdvsAReporte;
                arrayIdMDVReporte.value = mdvs.value.map(element => element.value);
                

                if(arrayIdMDVReporte.value.length){
                    return 100; 
                }else{
                    return 0;
                }
            };
            const getIdTactica = () => {
                const value = pasoHito.value + 1;
                if (pasoHito.value < 10) {
                    return ("H0" + (value).toString());
                }
                else {
                    return ("H" + (value).toString());
                }
            };
            const id_tactica = ref();
            const idTactica = computed((getIdTactica));
            const porcentajeLogro = computed((calculoAvance));

            const model = computed({
                get:() => {
                    mdvs.value = props.mdvs;
                    hitos.value = props.hitos;
                    identificador.value = props.identificador;
                    calculoAvance();
                    //porcentajeLogro.value = computed((calculoAvance));
                }
            });
            

            const validaPasoAtras = () =>{
                if(pasoHito.value > 0){
                    return true;
                }else{
                    return false;
                }
            };

            const validaPasoAdelante = () => {
                if(pasoHito.value < acciones.value.detalleAccion.hitos.length - 1){
                    return true;
                }else{
                    return false;
                }
            };

            const cambioAtras = async () => {
                
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };
                
                await store.dispatch("reporte/actualizaNuevoReporteHito", reporteHito);
                pasoHito.value -= 1;

                if(nuevoReporte.value.nuevoReporteHitos.length){
                    justificacion.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].justificacion_contingencia;
                    reporteJustificacion.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].reporte_justificacion_contingencia;
                    comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].comentario_cumplimiento;
                    indicadorLogro.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].indicador_logro;
                    idTactica.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].id_tactica;
                }else{
                    justificacion.value = "";
                    reporteJustificacion.value = "";
                    indicadorLogro.value = "";
                    comentario_cumplimiento.value = "";    
                    idTactica.value = getIdTactica();
                }

                descripcionTactica.value = hitos.value[pasoHito.value].label;
                porcentajeLogro.value = calculoAvance();
            };

            const cambioAdelante = async () => {
                
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                
                await store.dispatch("reporte/actualizaNuevoReporteHito", reporteHito);
                pasoHito.value += 1;
                
                if(pasoHito.value < (nuevoReporte.value.nuevoReporteHitos.length)){                    
                    justificacion.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].justificacion_contingencia;
                    reporteJustificacion.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].reporte_justificacion_contingencia;

                    comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].comentario_cumplimiento;
                    indicadorLogro.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].indicador_logro;
                    idTactica.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].id_tactica;
                }else{
                    justificacion.value = "";
                    reporteJustificacion.value = "";
                    indicadorLogro.value = "";
                    comentario_cumplimiento.value = "";    
                    idTactica.value = getIdTactica();
                }
                descripcionTactica.value = hitos.value[pasoHito.value].label;
                porcentajeLogro.value = calculoAvance();
            };

            const avanzaReporte = async () => {
                
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };
                
                await store.dispatch("reporte/actualizaNuevoReporteHito", reporteHito);
                store.dispatch("accion/limpiaDetalleAccion");
            };

            const pasoAtras = async () => {
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaNuevoReporteHito", reporteHito);

                store.dispatch("accion/reqFuncionesPorAccion", props.reporteAccion.accion);                
            };

            const validaPasoFuncionAtras = () => {
                if ((nuevoReporte.value.nuevoReporteFunciones.length) && (pasoHito.value === 0)){
                    return true;
                }else{
                    return false;
                }
            }

            const guardarAvance = async () => {
                await store.dispatch("reporte/actualizaNuevoReporteFuncionPMI", props.funciones[0].indicador_set[0].funcion);
                
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    justificacion_contingencia: justificacion.value,
                    reporte_justificacion_contingencia: reporteJustificacion.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };


                await store.dispatch("reporte/actualizaNuevoReporteHito", reporteHito);
                

                store.dispatch("reporte/postReporte", nuevoReporte.value.nuevoReporte);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");
                

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };


            if(nuevoReporte.value.nuevoReporteHitos.length){
                comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteHitos[0].comentario_cumplimiento;
                indicadorLogro.value = nuevoReporte.value.nuevoReporteHitos[0].indicador_logro;
                
                justificacion.value = nuevoReporte.value.nuevoReporteHitos[0].justificacion_contingencia;
                reporteJustificacion.value = nuevoReporte.value.nuevoReporteHitos[0].reporte_justificacion_contingencia;
            };

            return { 
                opcionesJustificacion,
                validaPasoAtras,
                validaPasoAdelante,
                pasoAtras,
                validaPasoFuncionAtras,
                cambioAtras,
                cambioAdelante,
                avanzaReporte,
                nuevoReporte,
                guardarAvance,

                idTactica,
                arrayIdMDVReporte,
                acciones,
                hitosIngresados,
                detalleProductos,
                mdvs,
                hitos,
                reporteJustificacion,
                justificacion,
                id_tactica: toRef(props, "stepPasoHito"), 
                
                porcentajeLogro,
                porcentaje,
                pasoHito,
                model,
                indicadorLogro,
                comentario_cumplimiento,
                
                descripcionTactica,
                identificador,
                fechaFormateada: toRef(props, "fechaFormateada"),
            }
        }
    })
</script>