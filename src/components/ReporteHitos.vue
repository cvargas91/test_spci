<template>
    <!--<q-card 
        style="width:100%"
        flat bordered
    >-->
    <div align="center">
        <div class="q-pa-md q-gutter-sm" style="width:65%">
            <p align="left">
                <b>1.- Evaluación entrega a Medios de Verificación</b>
            </p>
        </div> 
        <q-card 
            style="width:65%"
            flat bordered
        >
            
            <q-card-section horizontal style="height: 40px">
                <q-item-label class="col-1 bg-blue-2" flat bordered>
                    <b>Hito</b>
                </q-item-label>
                <q-separator vertical />
                <q-item-label class="col-2 bg-deep-orange-1" flat bordered>

                    {{idTactica}}
                </q-item-label>
                <q-separator vertical />
                <q-item-label class="col bg-deep-orange-1" flat bordered>
                    {{descripcionTactica}}
                </q-item-label>
            </q-card-section>

            <q-separator horizontal/>

            <q-card-section horizontal style="height: 20px">
                <q-item-label class="col bg-blue-2" flat bordered>
                    <b>MDV</b>
                </q-item-label>
                <q-separator vertical/>
                <q-item-label class="col-2 bg-blue-2" flat bordered>
                    <b>Logro</b>
                </q-item-label>
                <q-separator vertical/>
                <q-item-label class="col-2 bg-blue-2" flat bordered>
                    <b>Indicador de Logro</b>
                </q-item-label>
                <q-separator vertical/>
                <q-item-label class="col bg-blue-2" flat bordered>
                    <b>Comentario al cumplimiento</b>
                </q-item-label>
            </q-card-section>

            <q-separator horizontal/>
            
            <q-card-section 
                horizontal 
                style="min-height: 50px"
            >
                
                <q-item-label class="col" flat bordered v-model="model">
                    <q-expansion-item
                        expand-icon-toggle
                        expand-separator
                        label="Detalle MDVs"
                        :caption="identificador"
                    >
                        <div v-for="(hitoEnReporte) in acciones.detalleMDVAReporte" :key="hitoEnReporte.id" style="word-wrap:break-word">
                            {{identificador}}_{{idTactica}}_{{hitoEnReporte.label}}
                        </div>
                    </q-expansion-item>                    
                </q-item-label>
                <q-separator vertical />
                <q-item-label class="col-2" flat bordered>
                    <q-input
                        input-class="text-right"
                        v-model="porcentajeLogro"
                        borderless
                        suffix="%"
                        readonly  
                    />
                </q-item-label>
                <q-separator vertical />
                <q-item-label class="col-2" flat bordered>
                    <q-select
                        v-model="indicadorLogro" 
                        :options="opcionesLogro" 
                        label="No logrado/Logrado con atraso/Logrado" 
                        style="width: 100%"
                    />
                </q-item-label>
                <q-separator vertical />
                <q-item-label class="col" flat bordered>
                    <q-input
                        style="height: auto"
                        v-model="comentario_cumplimiento"
                        borderless
                        type="textarea"
                        label="Ingresar comentario al cumplimiento"
                    />
                </q-item-label>
            </q-card-section>                            
        </q-card>
    </div>
    <q-space />
    <br/>
    <q-space />
    <br/>
    <q-separator inset />
    <div class="row justify-end q-gutter-sm q-ma-md">
        <BotonCancelarReporte 
            opcion="hito"
            @guardarAvance="guardarAvance"
        />

        <!--<q-btn
            class="q-ml-sm"
            color="btnCancelar"
            label="   Cancelar   "
            @click="cancelarReporte"
        />-->
        <q-btn
            v-if="validaPasoFuncionAtras()"
            color="btnVolver"
            @click="pasoAtras"
            label=" Volver a Funciones  "
            class="q-ml-sm"
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
    
    <q-space />
    <br/>
</template>
<script>
    import { ref,toRef, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";

    export default defineComponent({        
        components:{
            BotonCancelarReporte,
        },
        props: {
            identificador: String,
            mdvs: Array,
            hitos: Array,
            reporteAccion: Object,
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
            const opcionesLogro = ['No logrado','Logrado con atrasos','Logrado'];
            
        
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
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaNuevoReporteHito", reporteHito);
                pasoHito.value -= 1;

                if(nuevoReporte.value.nuevoReporteHitos.length){
                    comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].comentario_cumplimiento;
                    indicadorLogro.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].indicador_logro;
                    idTactica.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].id_tactica;
                }else{
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
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaNuevoReporteHito", reporteHito);
                pasoHito.value += 1;

                if(pasoHito.value < (nuevoReporte.value.nuevoReporteHitos.length)){                    
                    comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].comentario_cumplimiento;
                    indicadorLogro.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].indicador_logro;
                    idTactica.value = nuevoReporte.value.nuevoReporteHitos[pasoHito.value].id_tactica;
                }else{
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
                
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : idTactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
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
            };

            return { 
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

                id_tactica: toRef(props, "stepPasoHito"), 
                
                porcentajeLogro,
                porcentaje,
                pasoHito,
                model,
                indicadorLogro,
                comentario_cumplimiento,
                
                opcionesLogro,
                descripcionTactica,
                identificador,
            }
        }
    })
</script>