import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { NgZorroAntdModule } from 'ng-zorro-antd';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';

// /** 注册语言包 ** /
import { registerLocaleData } from '@angular/common';
import zh from '@angular/common/locales/zh';
import { DirectoryComponent } from './directory/directory.component';
registerLocaleData(zh);

@NgModule({
  declarations: [
    AppComponent,
    DirectoryComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    NgZorroAntdModule.forRoot()
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
