<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>请选择部位：</span>
            <el-select v-model="companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
            <el-select v-model="dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
            <el-select v-model="buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
            <br>
            <span>请选择日期：</span>
            <el-date-picker v-model="insp_date" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>
            <br>
            <span>巡检人姓名：</span>
            <el-input
              placeholder="请输入巡检人姓名"
              v-model="insp_emp"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getInspects" type="primary">查询</el-button>
      <el-button @click="insert" type="primary">新增巡检</el-button>
    </div>

    <el-collapse v-model="activeNames">
      <el-collapse-item  v-for="item in insp_table" :key="item.index" :title="item.title" :name="item.name">
        <el-table
          :data="item.data"
          border
          style="width: 100%">
          <el-table-column
            fixed
            prop="insp_date"
            label="巡检日期"
            width="150">
          </el-table-column>
          <el-table-column
            prop="insp_emp"
            width="200"
            label="巡检人">
          </el-table-column>
          <el-table-column
            prop="buwei_name"
            width="200"
            label="部位名称">
          </el-table-column>
          <el-table-column
            prop="is_qualified"
            label="是否合格"
            width="100"
            :formatter="formatter">
          </el-table-column>
          <el-table-column
            prop="description"
            label="描述">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="100">
            <template slot-scope="scope">
              <el-button @click="remove(scope.row)" type="text" size="mini" icon="el-icon-delete"></el-button>
              <el-button @click="edit(scope.row)" type="text" size="mini" icon="el-icon-edit"></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
    </el-collapse>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="right" label-width="100px">
        <template v-if="title === '新增巡检'">
          <el-form-item label="公司名称">
            <el-select v-model="companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体">
            <el-select v-model="dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位">
            <el-select v-model="buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="巡检类型">
            <el-select v-model="type" filterable clearable placeholder="请选择巡检类型">
              <el-option
                v-for="(val, key, index)  in insp_types"
                :key="index"
                :label="key"
                :value="val">
              </el-option>
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="巡检日期">
          <el-date-picker v-model="insp_date" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>          
        </el-form-item>
        <el-form-item label="巡检人">
          <el-input
            placeholder="请输入巡检人姓名"
            v-model="insp_emp"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="是否合格">
          <el-select v-model="is_qualified" filterable clearable placeholder="请选择是否合格">
            <el-option
              label="是"
              :value=true>
            </el-option>
            <el-option
              label="否"
              :value=false>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            type="textarea"
            :rows="2"
            placeholder="请输入内容"
            v-model="description">
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitData">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  export default {
    mounted(){
      this.$store.dispatch('inspect/buwei/getCompanies')
    },

    data() {
      return {
        companyid: '',
        dantiid: '',
        buweiid: null,
        insp_id: null,
        insp_date: null,
        insp_emp: null, 
        type: null,        
        is_qualified: null,
        description: '',
        insp_types: {质量巡检:'quality_inspect',安全巡检:'safety_inspect',产品巡检:'produce_inspect'},             
        activeNames: ['1'],
        dialogVisible: false,
        title: '',
      }
    },

    methods: {
      // 用于格式化is_qualified的值
      formatter(row, column) {
        return row.is_qualified ? '合格' : '不合格';
      },
      getInspects(){
          this.$store.dispatch('inspect/getInspects', 
          { "buweiid":this.buweiid, "insp_date":this.insp_date, "insp_emp":this.insp_emp })        
      },
      insert(){
        this.title = '新增巡检'
        this.dialogVisible = true
      },
      edit(data){
        this.insp_id = data.id
        this.type = data.type
        this.title = '编辑巡检'
        this.insp_date = data.insp_date
        this.insp_emp = data.insp_emp
        this.is_qualified = data.is_qualified
        this.description = data.description
        this.dialogVisible = true
      },
      submitData(){
        var data = {
          type:this.type,
          buweiid:this.buweiid,
          insp_date:this.insp_date,
          insp_emp:this.insp_emp,
          description:this.description,
          is_qualified:this.is_qualified,
        }
        if(this.title === '新增巡检'){
          this.$store.dispatch('inspect/postInspects',data)
        }
        else if(this.title === '编辑巡检'){
          data["id"] = this.insp_id
          this.$store.dispatch('inspect/putInspects',data)
        }
        this.dialogVisible = false
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('inspect/removeInspects',data);
        }).catch(() => {         
        });
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      }
    },

    computed: {
      ...mapGetters('inspect/buwei',{
        'dantis':'dantis',
        'companies':'companies',
        'buweis':'buweis',
        }
      ),
      ...mapGetters('inspect',{
        'quality_inspects':'quality_inspects',
        'safety_inspects':'safety_inspects',
        'produce_inspects':'produce_inspects',
		  }),
      insp_table(){
        return [
          {title:"质量巡检", name:"2", data:this.quality_inspects},
          {title:"安全巡检", name:"3", data:this.safety_inspects},
          {title:"产品巡检", name:"4", data:this.produce_inspects},
        ]
      },
    },

    watch:{
      companyid: function(){
        this.dantiid = ''
        this.$store.commit('inspect/buwei/setDantis',[])
        if(Boolean(this.companyid)){
          this.$store.dispatch('inspect/buwei/getDantis', this.companyid)
        }
      },
      dantiid: function(){
        this.buweiid = ''
        this.$store.commit('inspect/buwei/setBuweis',[])
        if(Boolean(this.dantiid)){
          this.$store.dispatch('inspect/buwei/getBuweis', this.dantiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .el-select {
    width: 200px;
    margin-bottom: 20px;
  }
  .select {
    width: 700px;
    margin-right: 20px;
    display: inline-block;
  }
  .el-input {
    width: 200px;
    margin-bottom: 20px;
  }
  .el-form-item {
    margin-bottom: 0px;
  }
  .el-textarea {
    width: 200px;
  }
</style>

<style>
  .el-dialog {
    width: 385px !important;
  }
  .el-table {
    margin-top: 5px;
  }
  .el-collapse-item__header {
    width: 120px;
    font-size: 16px;
    color: #409eff;
  }
</style>
