<template>
  <form>
    <md-dialog-alert :md-active.sync="popupdialog" :md-content="dialogcontent" md-confirm-text="好" />
    <md-card>
      <md-card-header :data-background-color="dataBackgroundColor">
        <h4 class="title">新库存商品</h4>
        <p class="category">手动新建库存商品</p>
      </md-card-header>

      <md-card-content>
        <div class="md-layout">
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>名称</label>
              <md-input v-model="name" type="text"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-33">
            <md-field>
              <label>数量</label>
              <md-input v-model="count" type="number"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100 md-size-50">
            <md-field>
              <label>仓库</label>
              <md-input v-model="place" type="text"></md-input>
            </md-field>
          </div>
          <div class="md-layout-item md-size-100 text-right">
            <md-button class="md-raised md-success" v-on:click="newuser($event)">创建商品</md-button>
          </div>
        </div>
      </md-card-content>
    </md-card>
  </form>
</template>
<script>
import Cookies from "js-cookie";
import Vue from "vue";
import VueResource from "vue-resource";
Vue.use(VueResource);
export default {
  name: "new-user-form",
  props: {
    dataBackgroundColor: {
      type: String,
      default: ""
    }
  },
  data: function() {
    return {
      dialogcontent: "",
      popupdialog: false,
      name: null,
      count: 0,
      place: null
    };
  },
  methods: {
    newuser: function(e) {
      Vue.http
        .get("/new_store_item", {
          params: {
            name: this.name,
            number: this.count,
            place: this.place
          }
        })
        .then(response => {
          window.console.log(response.body);
          if (response.body == "ok") {
            this.dialogcontent = "创建成功";
            this.dialogDismiss = function() {
              location.reload();
              this.dialogDismiss = function() {};
            };
            this.popupdialog = true;
          } else {
            this.dialogcontent = "创建失败";
            this.popupdialog = true;
          }
        });
    },
    dialogDismiss: function() {}
  },
  watch: {
    popupdialog: {
      handler(newName, oldName) {
        if (newName == false) {
          this.dialogDismiss();
        }
      }
    }
  }
};
</script>
<style></style>
