import axios from 'axios'

const state = {
    quality_inspects:[],
    safety_inspects:[],
    produce_inspects:[],
}

const getters = {
    quality_inspects:state=>{
        return state.quality_inspects
    },
    safety_inspects:state=>{
        return state.safety_inspects
    },
    produce_inspects:state=>{
        return state.produce_inspects
    }
}

const  mutations = {
    setQualityInspects(state, data){
        state.QualityInspects = data
    },
    removeQualityInspects(state,data){
        var index = state.QualityInspects.indexOf(data)
        state.QualityInspects.splice(index,1)
    },
    setSafetyInspects(state, data){
        state.SafetyInspects = data
    },
    removeSafetyInspects(state,data){
        var index = state.SafetyInspects.indexOf(data)
        state.SafetyInspects.splice(index,1)
    },
    setProduceInspects(state, data){
        state.ProduceInspects = data
    },
    removeProduceInspects(state,data){
        var index = state.ProduceInspects.indexOf(data)
        state.ProduceInspects.splice(index,1)
    },
}

const actions = {
    getInspects(context,data){
        axios.get(`/kong/gongdi_mng/v1.0/dantis/${data}/Inspects`)
        .then(response=>{
            if(response.status === 200){
                context.commit('setInspects',response.data)
            }
        })
    },
    // postBuwei(context,data){
    //     axios.post('/kong/gongdi_mng/v1.0/buweis',data)
	// 	.then(response => {
    //         if (response.status === 201) {
    //             data = context.getters.buweis 
    //             data.unshift(response.data)
    //             context.commit('setBuweis', data)
    //         }
    //         else {
    //             alert('新增失败')
    //         }
	// 	}).catch(function(error){
	// 		alert('请求失败')
	// 	})
    // },
    // putBuweis(context,data){
    //     console.table(data)
    //     delete data.danti_name
    //     delete data.dantiid
    //     axios.put(`/kong/gongdi_mng/v1.0/buweis/${data.id}`,data)
    //     .then(response => {
    //         if(response.status === 201){
    //             for(var item of context.getters.buweis){
    //                 if(item.id === data.id){
    //                     var index = context.getters.buweis.indexOf(item)
    //                     var [...newDatas] = context.getters.buweis
    //                     newDatas.splice(index, 1, response.data)
    //                     context.commit('setBuweis',newDatas)
    //                     break
    //                 }
    //             }
    //         }
    //     })
    //     .catch(error => {
    //         alert('出错')
    //     })
    // },
    // removeBuweis(context,data){
    //     axios.delete(`/kong/gongdi_mng/v1.0/buweis/${data.id}`)
	// 		.then(function(response){
    //             if(response.status === 204){
    //                 context.commit('removeBuweis',data)
    //             }
	// 		}).catch(function(error){
	// 		})
    // }
}

export default {
    state,
    getters,
    mutations,
    actions
}