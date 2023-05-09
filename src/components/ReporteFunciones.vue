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
                        <q-item-label  class="col-1 bg-blue-2" flat bordered><b>Función</b></q-item-label>
                        <q-separator vertical />
                        <q-item-label  class="col-2 bg-deep-orange-1" flat bordered v-model="model">
                        
                            {{idTactica}}
                        </q-item-label>
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
                    
                    ><!--v-model="model"-->
                    <q-item-label class="col-3" flat bordered v-model="model">
                        <q-expansion-item
                            expand-icon-toggle
                            expand-separator
                            label="Detalle MDVs"
                            :caption="identificador"
                        >
                            <div v-for="(indicador) in funciones[pasoFuncion].indicador_set" :key="indicador.id">
                                {{identificador}}_{{idTactica}}_{{indicador.nombreVerificador}}
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
    <!--</q-card>-->
</template>
<script>
    import { ref,toRef,watch, computed, onMounted, onUnmounted, defineComponent } from "vue";
    import { useStore } from "vuex";
    import { useRouter } from "vue-router";
    import BotonCancelarReporte from "src/components/BotonCancelarReporte.vue";

    export default defineComponent({
    components:{
        BotonCancelarReporte,
    },
    props: {
        identificador: String,
        funciones: Array,
        reporteAccion: Object,
    },
    watch: {        
            reporteAccion: async function (newValue, oldValue) {
                this.pasoFuncion = 0;

                if(newValue.reporte_funciones.length){
                    this.comentario_cumplimiento = newValue.reporte_funciones[0].comentario_cumplimiento;
                }else{
                    this.comentario_cumplimiento = "";
                }
            },
            funciones: function (newValue, oldValue) {                
                this.funciones = newValue;
                this.descripcionTactica = this.funciones[0].nombre;
            },
    },
    emits: ["cambioFuncion"],
    setup(props, { emit }) {
        const store = useStore();
        const router = useRouter();
        const nuevoReporte = computed(() => store.state.reporte);
        const acciones = computed(() => store.state.accion);
    
        const funciones = ref(props.funciones);
        const descripcionTactica = ref(funciones.value[0].nombre);

        const meta = ref();
        const avance = ref();
        
        const id_tactica = ref();
        
        const entregas = computed(() => store.state.verificador);
        const verificador = ref("");
        const comentario_cumplimiento = ref("");
        
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

        const calculoAvance = () => {
            var auxiliarIndicador;
            if(funciones.value[pasoFuncion.value].indicador_set.length);
                auxiliarIndicador = funciones.value[pasoFuncion.value].indicador_set[0].id;

            store.dispatch("verificador/reqVerificadorPorIndicador", auxiliarIndicador);
            store.dispatch("reporte/reqTotalMetasPorFuncion", funciones.value[pasoFuncion.value].indicador_set[0].funcion);

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
        const idTactica = computed((getIdTactica));
        const labelMetaAvance = ref("");
        const mostrar = ref("");
        const indicadores = ref(funciones.value[0]);

        const model = computed({
            get: () => {
                funciones.value = props.funciones;
            }            
        });
    

        const validaPasoAtras = () =>{
            if(pasoFuncion.value > 0){
                return true;
            }else{
                return false;
            }
        };
        const validaPasoAdelante = () => {
            if(pasoFuncion.value < acciones.value.funciones.length-1){
                return true;
            }else{
                return false;
            }
        };

        const cambioAtras = async () => {
            

            const reporteFuncion = {
                id_tactica : idTactica.value,
                funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                indicador : indicadorAvance.value,
                comentario_cumplimiento : comentario_cumplimiento.value
            };

            
            await store.dispatch("reporte/actualizaNuevoReporteFuncion", reporteFuncion);
            pasoFuncion.value -= 1;

            if(nuevoReporte.value.nuevoReporteFunciones.length){
                comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteFunciones[pasoFuncion.value].comentario_cumplimiento;
                idTactica.value = nuevoReporte.value.nuevoReporteFunciones[pasoFuncion.value].id_tactica;
            }else{
                comentario_cumplimiento.value = "";    
                idTactica.value = getIdTactica();
            }
            
            descripcionTactica.value = funciones.value[pasoFuncion.value].nombre;
            indicadorAvance.value = calculoAvance();
        };

        const cambioAdelante = async () => {
            
            const reporteFuncion = {
                id_tactica : idTactica.value,
                funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                indicador : indicadorAvance.value,
                comentario_cumplimiento : comentario_cumplimiento.value
            };

            
            
            await store.dispatch("reporte/actualizaNuevoReporteFuncion", reporteFuncion);
            pasoFuncion.value += 1;

            if(pasoFuncion.value < (nuevoReporte.value.nuevoReporteFunciones.length)){
                comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteFunciones[pasoFuncion.value].comentario_cumplimiento;
                idTactica.value = nuevoReporte.value.nuevoReporteFunciones[pasoFuncion.value].id_tactica;
            }else{
                comentario_cumplimiento.value = "";    
                idTactica.value = getIdTactica();
            }
            
            descripcionTactica.value = funciones.value[pasoFuncion.value].nombre;
            indicadorAvance.value = calculoAvance();
        };

        const avanzaReporte = async () => {
                
            const reporteFuncion = {
                id_tactica : idTactica.value,
                funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                indicador : indicadorAvance.value,
                comentario_cumplimiento : comentario_cumplimiento.value
            };

            await store.dispatch("reporte/actualizaNuevoReporteFuncion", reporteFuncion);
            store.dispatch("accion/limpiaFunciones");
        };

        const guardarAvance = async () => {
            
            
            const reporteFuncion = {
                id_tactica : idTactica.value,
                funcion : funciones.value[pasoFuncion.value].indicador_set[0].funcion,
                indicador : indicadorAvance.value,
                comentario_cumplimiento : comentario_cumplimiento.value
            };

            await store.dispatch("reporte/actualizaNuevoReporteFuncion", reporteFuncion);

            store.dispatch("reporte/postReporte", nuevoReporte.value.nuevoReporte);
            store.dispatch("reporte/limpiaReporteFunciones");
            store.dispatch("reporte/limpiaReporteHitos");
            store.dispatch("reporte/limpiaReporteAccion");
                

            store.dispatch("reporte/reqReportesBorradores");
            store.dispatch("reporte/reqReportesUpci");

            router.push("panelReportesUpci");
        };


        if(nuevoReporte.value.nuevoReporteFunciones.length){
            comentario_cumplimiento.value = nuevoReporte.value.nuevoReporteFunciones[0].comentario_cumplimiento;
        }


        return {
            validaPasoAtras,
            validaPasoAdelante,
            cambioAtras,
            cambioAdelante,
            avanzaReporte,
            funciones,
            guardarAvance,
            //getIdTactica,
            
            idTactica,
            meta: computed(() => store.state.reporte.total_meta),
            avance: computed(() => store.state.verificador.avance),
            labelMetaAvance,
            indicadorAvance,
            entregas,
            
            pasoFuncion,
            nuevoReporte,
            
            comentario_cumplimiento,
            descripcionTactica,
            id_tactica,
            indicadores,
            identificador: toRef(props, "identificador"),
            model,
            mostrar,
            acciones,
        };
    },
})
</script>