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
                <q-card-section horizontal style="height:auto;">                    
                    <q-item-label  class="col-1 bg-blue-2" flat bordered>
                        <b>Función</b>
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-labeln  class="col-2 bg-deep-orange-1" flat bordered v-model="model">
                        {{id_tactica}} 
                    </q-item-labeln>
                    <q-separator vertical />
                    <q-item-label  class="col bg-deep-orange-1" flat bordered > 
                        {{descripcionTactica}} 
                    </q-item-label>
                </q-card-section>

                <q-separator horizontal />

                <q-card-section horizontal style="height: 20px">
                    <q-item-label class="col-3 bg-blue-2" flat bordered>
                        <b>MDV</b>
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-label class="col-3 bg-blue-2" flat bordered>
                        <b>Indicador de Avance</b>
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-label class="col bg-blue-2" flat bordered>
                        <b>Comentario al cumplimiento</b>
                    </q-item-label>
                </q-card-section>

                <q-separator horizontal />
                <q-card-section 
                    horizontal 
                    style="height: auto"
                >
                    <q-item-label class="col-3" flat bordered>

                        <q-expansion-item
                            expand-icon-toggle
                            expand-separator
                            label="Detalle MDVs"
                            :caption="identificador"
                        >
                            <div v-for="(indicador) in funciones[pasoFuncion].indicador_set" :key="indicador.id">
                                {{identificador}}_{{id_tactica}}_{{indicador.nombreVerificador}}
                            </div>                     
                        </q-expansion-item>
                    </q-item-label>
                    <q-separator vertical />
                    <q-item-label class="col-3" flat bordered >
                        
                        <q-input
                                :label="labelMetaAvance"
                                input-class="text-right"
                                v-model="indicadorAvance"    
                                borderless
                                suffix="%"
                                readonly  
                        >
                        
                        </q-input>
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
            opcion="funcion"
            @guardarAvance="guardarAvance" 
        />
        <!--<q-btn
            class="q-ml-sm"
            color="btnCancelar"
            label="   Cancelar   "
            @click="cancelarReporte"
        />-->
        <q-btn
            v-if="validaPasoAtras()"
            color="btnVolver"
            @click="cambioAtras"
            label=" Función Anterior  "
            class="q-ml-sm"
        />
        <q-btn
            v-if="validaPasoAdelante()"
            color="btnContinuar"
            @click="cambioAdelante"
            label="   Siguiente Función   "
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
    import { ref, toRef, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";    
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";

    export default defineComponent({        
        components:{
            BotonCancelarReporte,
        },
        props:{
            reporteAccion: Object,
            reporteFunciones: Array,
            identificador: String,
        },
        watch: {        
            /*reporteAccion: async function (newValue, oldValue) {
                

                const reporteFuncion = {
                    id_tactica : this.id_tactica,
                    funcion : this.funciones.value[this.pasoFuncion].indicador_set[0].funcion,
                    indicador : this.indicadorAvance,
                    comentario_cumplimiento : this.comentario_cumplimiento
                };

                await this.$store.dispatch("reporte/actualizaReporteFunciones", reporteFuncion);
                this.$store.dispatch("accion/limpiaFunciones");
            },*/
        },
        setup(props) { 
            const store = useStore();
            const router = useRouter();
        
            const reporteFunciones = computed(() => store.state.reporte);
            const acciones = computed(() => store.state.accion);
            const funciones = ref(acciones.value.funciones);
            const descripcionTactica = ref(funciones.value[0].nombre);
            const meta = ref();
            const avance = ref();
            
            const entregas = computed (() => store.state.verificador);
            const verificador = ref('');            
                        
            const pasoFuncion = ref(0);
            const getIdTactica = () => {
                const value = pasoFuncion.value + 1;
                if (pasoFuncion.value < 10) {
                    return ("F0" + (value).toString());
                }
                else {
                    return ("F" + (value).toString());
                }
            };
            const calculoAvance  = () => {            
                var auxiliarIndicador;
                var funcion;

                if(reporteFunciones.value.reporteFuncionesAEditar.length){
                    funcion = reporteFunciones.value.reporteFuncionesAEditar[pasoFuncion.value].funcion;
                }else{
                    funcion = funciones.value[pasoFuncion.value].indicador_set[0].funcion;
                }

                if(funciones.value[pasoFuncion.value].indicador_set.length);
                    auxiliarIndicador = funciones.value[pasoFuncion.value].indicador_set[0].id;
                
                store.dispatch("verificador/reqVerificadorPorIndicador", auxiliarIndicador);
                store.dispatch("reporte/reqTotalMetasPorFuncion", funcion);
                
                let metaFuncion = (computed(() => store.state.reporte.total_meta)).value;
                let avanceFuncion = (computed(() => store.state.verificador.avance)).value;
                
                if(avanceFuncion){
                    labelMetaAvance.value = "Meta (" + metaFuncion + ") / Avance ("+ avanceFuncion + ")";
                    return (Math.floor((avanceFuncion/metaFuncion)*100));
                }else {
                    labelMetaAvance.value = "Meta (" + metaFuncion + ") / Avance ("+ 0 + ")";
                    return (Math.floor((0/metaFuncion)*100));
                }
            };

            const indicadorAvance = computed((calculoAvance));
            const labelMetaAvance = ref('');
            const mostrar = ref('');

            const id_tactica = computed((getIdTactica));
            const comentario_cumplimiento = ref("");
            const indicadores = ref(funciones.value[0]);
            
            const model = computed({
                get:() => {
                    
                    if(reporteFunciones.value.reporteFuncionesAEditar.length){
                    
                        comentario_cumplimiento.value = reporteFunciones.value.reporteFuncionesAEditar[0].comentario_cumplimiento;
                        id_tactica.value = reporteFunciones.value.reporteFuncionesAEditar[0].id_tactica;
                    }else{
                    
                        comentario_cumplimiento.value = "";
                        id_tactica.value = getIdTactica();
                    }
                    pasoFuncion.value = 0;
                    funciones.value = acciones.value.funciones;
                    descripcionTactica.value = funciones.value[0].nombre;
                }
            });

            const  cambioAdelante = async () => {
                

                const reporteFuncion = {
                    id_tactica : id_tactica.value,
                    funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                    indicador : indicadorAvance.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteFunciones", reporteFuncion);

                pasoFuncion.value += 1;

                if(pasoFuncion.value < (reporteFunciones.value.reporteFuncionesAEditar.length)){
                    comentario_cumplimiento.value = reporteFunciones.value.reporteFuncionesAEditar[pasoFuncion.value].comentario_cumplimiento;
                    id_tactica.value = reporteFunciones.value.reporteFuncionesAEditar[pasoFuncion.value].id_tactica;
                }else{
                    comentario_cumplimiento.value = "";
                    id_tactica.value = getIdTactica();
                }
                                
                descripcionTactica.value = funciones.value[pasoFuncion.value].nombre;
                indicadorAvance.value = calculoAvance();
            };

            const cambioAtras = async () => {
                

                const reporteFuncion = {
                    id_tactica : id_tactica.value,
                    funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                    indicador : indicadorAvance.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteFunciones", reporteFuncion);
                pasoFuncion.value -= 1;

                comentario_cumplimiento.value = reporteFunciones.value.reporteFuncionesAEditar[pasoFuncion.value].comentario_cumplimiento;
                id_tactica.value = reporteFunciones.value.reporteFuncionesAEditar[pasoFuncion.value].id_tactica;
                descripcionTactica.value = funciones.value[pasoFuncion.value].nombre;
                indicadorAvance.value = calculoAvance();
            };

            const avanzaReporte = async () => {
                
                
                const reporteFuncion = {
                    id_tactica : id_tactica.value,
                    funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                    indicador : indicadorAvance.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteFunciones", reporteFuncion);
                store.dispatch("accion/limpiaFunciones");
            };

            const guardarAvance = async () => {
                
                const reporteFuncion = {            
                    id_tactica : id_tactica.value,
                    funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                    indicador : indicadorAvance.value,
                    comentario_cumplimiento : comentario_cumplimiento.value
                };

                await store.dispatch("reporte/actualizaReporteFunciones", reporteFuncion);

                
                store.dispatch("reporte/patchReporte", reporteFunciones.value.aEditar);
                store.dispatch("reporte/limpiaReporteFunciones");
                store.dispatch("reporte/limpiaReporteHitos");
                store.dispatch("reporte/limpiaReporteAccion");

                store.dispatch("reporte/reqReportesBorradores");
                store.dispatch("reporte/reqReportesUpci");

                router.push("panelReportesUpci");
            };

            const validaPasoAdelante = () => {
                if(pasoFuncion.value < funciones.value.length - 1){
                    return true;
                }else{
                    return false;
                }
            };

            const validaPasoAtras = () => {
                if(pasoFuncion.value > 0){
                    return true;
                }else{
                    return false;
                }
            };

            if(reporteFunciones.value.reporteFuncionesAEditar.length){
                
                id_tactica.value = reporteFunciones.value.reporteFuncionesAEditar[0].id_tactica;
                comentario_cumplimiento.value = reporteFunciones.value.reporteFuncionesAEditar[0].comentario_cumplimiento;
            }

            return {
                validaPasoAdelante,
                validaPasoAtras,
                cambioAdelante,
                cambioAtras,
                avanzaReporte,


                meta: computed(() => store.state.reporte.total_meta),
                avance: computed(() => store.state.verificador.avance),
                labelMetaAvance,
                indicadorAvance,
                entregas,
                reporteFunciones,
                guardarAvance,
                pasoFuncion,
                funciones,
                
                comentario_cumplimiento,
                descripcionTactica,
                id_tactica,
                indicadores,
                identificador: toRef(props, "identificador"),
                model,
                mostrar,
                acciones,
            }
        }
    })
</script>