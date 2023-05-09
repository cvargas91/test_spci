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
                <q-separator vertical /><!---->
                <q-item-label class="col-2 bg-deep-orange-1" flat bordered ><!--v-model="model"-->
                    {{id_tactica}}
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
                            {{identificador}}_{{id_tactica}}_{{hitoEnReporte.label}}
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
            reporteAccion: Object,
            identificador: String,
        },
        watch: {        
            /*reporteAccion: async function (newValue, oldValue) {
                
                await this.$store.dispatch("reporte/setReporteHitosAEditar", oldValue.reporte_hitos);
                await this.$store.dispatch("reporte/setReporteFuncionesAEditar", oldValue.reporte_funciones);

                const reporteHito = {
                    mdvs : this.arrayIdMDVReporte, 
                    hito: this.hitos[this.pasoHito].value,
                    id_tactica : this.id_tactica,
                    indicador : this.porcentajeLogro,
                    indicador_logro: this.indicadorLogro,
                    comentario_cumplimiento : this.comentario_cumplimiento
                };
                
                await this.$store.dispatch("reporte/actualizaReporteHitos", reporteHito);

                this.$store.dispatch("accion/reqFuncionesPorAccion", newValue.accion);
                await this.$store.dispatch("reporte/setReporteHitosAEditar", newValue.reporte_hitos);
                await this.$store.dispatch("reporte/setReporteFuncionesAEditar", newValue.reporte_funciones);
            },*/
        },
        setup(props) {   
            
            const store = useStore();
            const router = useRouter();
            const reporteHitos = computed(() => store.state.reporte);
            const acciones = computed(() => store.state.accion);
            const mdv = ref(acciones.value.detalleAccion.mdvs);
            const hitos = ref(acciones.value.detalleAccion.hitos);
            const opcionesLogro = ['No logrado','Logrado con atrasos','Logrado'];
            
            const reporteAccion = computed(() => store.state.reporte);

            const hitosIngresados = acciones.value.detalleAccion.hitos;
            
            const indicadorLogro = ref("");
            const comentario_cumplimiento = ref("");

            const detalleProductos = computed(() => store.state.producto.totalHitos);
            
            const descripcionTactica = ref('');
            
            const identificador = ref(props.identificador);
            
            const pasoHito =  ref(0);
            const arrayIdMDVReporte = ref('');

            const getIdTactica = () => {
                const value = pasoHito.value + 1;
                if (pasoHito.value < 10) {
                    return ("H0" + (value).toString());
                }
                else {
                    return ("H" + (value).toString());
                }
            };

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

            const idTactica = ref('');
            const id_tactica = computed((getIdTactica));

            const porcentajeLogro = computed((calculoAvance));

            const model = computed({
                get:() => {
                    mdv.value = acciones.value.detalleAccion.mdvs;
                    hitos.value = acciones.value.detalleAccion.hitos;

                    if(reporteHitos.value.reporteHitosAEditar.length){
                        comentario_cumplimiento.value = reporteHitos.value.reporteHitosAEditar[0].comentario_cumplimiento;
                        indicadorLogro.value = reporteHitos.value.reporteHitosAEditar[0].indicador_logro;
                        id_tactica.value = reporteHitos.value.reporteHitosAEditar[0].id_tactica;
                    }else{
                        comentario_cumplimiento.value = "";
                        indicadorLogro.value = "";
                        id_tactica.value = getIdTactica();
                    }

                    descripcionTactica.value = hitos.value[0].label;
                }
            });
            
            const  cambioAdelante = async () => {

                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : id_tactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };
                
                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);

                pasoHito.value += 1;

                if(pasoHito.value < (reporteHitos.value.reporteHitosAEditar.length)){
                    indicadorLogro.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].indicador_logro;
                    comentario_cumplimiento.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].comentario_cumplimiento;
                    id_tactica.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].id_tactica;
                }else{
                    indicadorLogro.value = "";
                    comentario_cumplimiento.value = "";
                    id_tactica.value = getIdTactica();
                }

                descripcionTactica.value = hitos.value[pasoHito.value].label;
                porcentajeLogro.value = calculoAvance();
            };

            const cambioAtras = async () => {                
                
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito : hitos.value[pasoHito.value].value,
                    id_tactica : id_tactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);
                pasoHito.value -= 1;


                comentario_cumplimiento.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].comentario_cumplimiento;
                id_tactica.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].id_tactica;
                indicadorLogro.value = reporteHitos.value.reporteHitosAEditar[pasoHito.value].indicador_logro;
                descripcionTactica.value = hitos.value[pasoHito.value].label;

                porcentajeLogro.value = calculoAvance();
            };

            const pasoAtras =  async () => {
                

                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : id_tactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);
                
                store.dispatch("accion/reqFuncionesPorAccion", reporteAccion.value.reporteAccionesAEditar.accion);
            };

            const avanzaReporte = async () => {
                
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : id_tactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);

                store.dispatch("accion/limpiaDetalleAccion");
            };


            const validaPasoAdelante = () => {
                if(pasoHito.value < acciones.value.detalleAccion.hitos.length - 1){
                    return true;
                }else{
                    return false;
                }
            };

            const validaPasoFuncionAtras = () => {
                if ((pasoHito.value === 0) && (reporteHitos.value.reporteFuncionesAEditar.length)){
                    return true;
                }else{
                    return false;
                }
            }

            const validaPasoAtras = () => {
                if(pasoHito.value > 0){
                    return true;
                }else{
                    return false;
                }
            };

            const guardarAvance = async () => {
                const reporteHito = {
                    mdvs : arrayIdMDVReporte.value, 
                    hito: hitos.value[pasoHito.value].value,
                    id_tactica : id_tactica.value,
                    indicador : porcentajeLogro.value,
                    indicador_logro: indicadorLogro.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteHitos", reporteHito);

                store.dispatch("reporte/patchReporte", reporteHitos.value.aEditar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };

            if (reporteHitos.value.reporteHitosAEditar.length){
                indicadorLogro.value = reporteHitos.value.reporteHitosAEditar[0].indicador_logro;
                comentario_cumplimiento.value = reporteHitos.value.reporteHitosAEditar[0].comentario;
            }
            
            return { 
                reporteHitos,
                cambioAdelante,
                cambioAtras,
                avanzaReporte,

                validaPasoAdelante,
                validaPasoAtras,
                validaPasoFuncionAtras,

                idTactica,
                arrayIdMDVReporte,
                acciones,
                hitosIngresados,
                detalleProductos,
                mdv,
                hitos,
                guardarAvance,
                id_tactica, 
                pasoAtras,
                porcentajeLogro,
                
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