<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>请选择部位：</span>
            <el-select v-model="filterData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
            <el-select v-model="filterData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
            <el-select v-model="filterData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
            <br>
            <span>请选择日期：</span>
            <el-date-picker v-model="filterData.insp_date" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>
            <br>
            <span>巡检人姓名：</span>
            <el-input
              placeholder="请输入巡检人姓名"
              v-model="filterData.insp_emp"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getInspects(1)" type="primary">查询</el-button>
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
            label="所属部位">
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
            width="130">
            <template slot-scope="scope">
              <el-button @click="remove(scope.row)" size="mini" icon="el-icon-delete"></el-button>
              <el-button @click="edit(scope.row)" size="mini" icon="el-icon-edit"></el-button>
            </template>
          </el-table-column>
        </el-table>

          <el-pagination
            v-show="Number(item.total_datas)"
            background
            layout="prev, pager, next"
            @current-change="(value) => handleCurrentChange(value, item.type)"
            :page-size="page_size"
            :page-count="item.total_pages">
          </el-pagination>

      </el-collapse-item>
    </el-collapse>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="right" label-width="100px" :model="formData" :rules="rules" ref="ruleForm">
        <template v-if="title === '新增巡检'">
          <el-form-item label="公司名称" prop="companyid">
            <el-select v-model="formData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体" prop="dantiid">
            <el-select v-model="formData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位" prop="buweiid">
            <el-select v-model="formData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="巡检类型" prop="type">
            <el-select v-model="formData.type" filterable clearable placeholder="请选择巡检类型">
              <el-option
                v-for="(val, key, index)  in insp_types"
                :key="index"
                :label="key"
                :value="val">
              </el-option>
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="巡检日期" prop="insp_date">
          <el-date-picker v-model="formData.insp_date" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>          
        </el-form-item>
        <el-form-item label="巡检人" prop="insp_emp">
          <el-input
            placeholder="请输入巡检人姓名"
            v-model="formData.insp_emp"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="是否合格" prop="is_qualified">
          <el-select v-model="formData.is_qualified" filterable clearable placeholder="请选择是否合格">
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
            v-model="formData.description">
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="resetForm('ruleForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('ruleForm')">确 定</el-button>
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
        rules: {
          companyid: [
            { required: true, message: '请选择所属公司', trigger: 'change' },
          ],
          dantiid: [
            { required: true, message: '请选择所属单体', trigger: 'change' },
          ],
          buweiid: [
            { required: true, message: '请选择所属部位', trigger: 'change' },
          ],
          type: [
            { required: true, message: '请选择巡检类型', trigger: 'change' },
          ],
          insp_date: [
            { required: true, message: '请选择巡检日期', trigger: 'blur' },
          ],
          insp_emp: [
            { required: true, message: '请输入巡检人', trigger: 'change' },
          ],
          is_qualified: [
            { required: true, message: '请选择是否合格', trigger: 'change' },
          ],
        },
        filterData:{
          companyid: "",
          dantiid: "",
          buweiid: null,
          insp_date: "",
          type: "",
        },
        formData:{
          companyid: "",
          dantiid: "",
          buweiid: null,
          type: "",    
          insp_date: "",
          insp_emp: "", 
          is_qualified: "",
          description: "",
        },
        page_size: 5,
        insp_id: null,
        quality_cur_page:1,
        safety_cur_page:1,
        produce_cur_page:1,
        insp_types: {质量巡检:'quality',安全巡检:'safety',产品巡检:'produce'},             
        activeNames: ['1','2','3','4'],
        dialogVisible: false,
        title: "",
      }
    },

    methods: {
      handleCurrentChange(val,type) {
        this.getInspects(val,[type])
        this[`${type}_cur_page`] = val
      },
      // 用于格式化is_qualified的值
      formatter(row, column) {
        return row.is_qualified ? '合格' : '不合格';
      },
      getInspects(page, insp_types=["quality", "safety", "produce"]){
          this.$store.dispatch('inspect/getInspects', 
          { "insp_types":insp_types, "buweiid":this.filterData.buweiid, "insp_date":this.filterData.insp_date, "insp_emp":this.filterData.insp_emp, "per_page":this.page_size, "page":page })        
      },
      insert(){
        // 新增时先清空表单数据        
        this.title = '新增巡检'
        this.dialogVisible = true
      },
      edit(data){
        // 点编辑时，将对应行数据写入表单   
        this.insp_id = data.id
        this.title = '编辑巡检'
        this.formData.buweiid = data.buweiid
        this.formData.type = data.type
        this.formData.insp_date = data.insp_date
        this.formData.insp_emp = data.insp_emp
        this.formData.is_qualified = data.is_qualified
        this.formData.description = data.description
        this.dialogVisible = true
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
        this.dialogVisible = false
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.submitData();
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      submitData(){
        // 组织表单需要的数据，创建或更新数据        
        var data = {
          type:this.formData.type,
          buweiid:this.formData.buweiid,
          insp_date:this.formData.insp_date,
          insp_emp:this.formData.insp_emp,
          is_qualified:this.formData.is_qualified,
          description:this.formData.description,
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
          var insp_type = data["type"]
          // 删除一条数据之后的页数
          var total_pages =  Math.ceil((this[`${insp_type}_total_datas`]-1) / this.page_size)
          this.$store.dispatch('inspect/removeInspects',data);
          // 解决删除数据后，当前页大于总页数的问题
          var page = this[`${insp_type}_cur_page`] > total_pages ? total_pages : this[`${insp_type}_cur_page`];
          this.getInspects(page,[insp_type])
        })
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
      }
    },

    computed: {
      quality_total_pages(){
        return Math.ceil(this.quality_total_datas / this.page_size)        
      },
      safety_total_pages(){
        return Math.ceil(this.safety_total_datas / this.page_size)        
      },
      produce_total_pages(){
        return Math.ceil(this.produce_total_datas / this.page_size)        
      },
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
        'quality_total_datas':'quality_total_datas',
        'safety_total_datas':'safety_total_datas',
        'produce_total_datas':'produce_total_datas',
		  }),
      insp_table(){
        return [
          {title:"质量巡检", name:"2", type:"quality", total_pages:this.quality_total_pages, total_datas:this.quality_total_datas, data:this.quality_inspects},
          {title:"安全巡检", name:"3", type:"safety", total_pages:this.safety_total_pages, total_datas:this.safety_total_datas, data:this.safety_inspects},
          {title:"产品巡检", name:"4", type:"produce", total_pages:this.produce_total_pages, total_datas:this.produce_total_datas, data:this.produce_inspects},
        ]
      },
    },

    watch:{
      "formData.companyid": function(){
        this.formData.dantiid = ''
        this.formData.buweiid = ''
        this.$store.commit('inspect/buwei/setDantis',[])
        this.$store.commit('inspect/buwei/setBuweis',[])
        if(Boolean(this.formData.companyid)){
          this.$store.dispatch('inspect/buwei/getDantis', {companyid:this.formData.companyid})
        }
      },
      "formData.dantiid": function(){
        this.formData.buweiid = ''
        this.$store.commit('inspect/buwei/setBuweis',[])
        if(Boolean(this.formData.dantiid)){
          this.$store.dispatch('inspect/buwei/getBuweis', this.formData.dantiid)
        }
      },
      "filterData.companyid": function(){
        this.filterData.dantiid = ''
        this.filterData.buweiid = ''
        this.$store.commit('inspect/buwei/setDantis',[])
        this.$store.commit('inspect/buwei/setBuweis',[])
        if(Boolean(this.filterData.companyid)){
          this.$store.dispatch('inspect/buwei/getDantis', {companyid:this.filterData.companyid})
        }
      },
      "filterData.dantiid": function(){
        this.filterData.buweiid = ''
        this.$store.commit('inspect/buwei/setBuweis',[])
        if(Boolean(this.filterData.dantiid)){
          this.$store.dispatch('inspect/buwei/getBuweis', this.filterData.dantiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .select .el-select {
    width: 200px;
    margin-bottom: 20px;
  } 
  .select {
    width: 700px;
    margin-right: 20px;
    display: inline-block;
  }
  .select .el-input {
    margin-bottom: 20px;
  }
  .el-input {
    width: 200px;
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
