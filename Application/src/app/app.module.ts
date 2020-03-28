import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ExplorerComponent } from './explorer/explorer.component';
import { DetailviewComponent } from './detailview/detailview.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

import { MatFormFieldModule } from '@angular/material/form-field';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material'
import { MatInputModule } from '@angular/material';
import { MatSelectModule } from '@angular/material';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTreeModule } from '@angular/material/tree';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDatepickerModule } from '@angular/material/datepicker'; 
import { MatNativeDateModule } from '@angular/material/core';

import { HttpClientModule } from '@angular/common/http';

import { ExerciseCompilerComponent } from './exercise-compiler/exercise-compiler.component';
import { DocumentEditorComponent } from './document-editor/document-editor.component';

@NgModule({
  declarations: [
    AppComponent,
    ExplorerComponent,
    DetailviewComponent,
    ExerciseCompilerComponent,
    DocumentEditorComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule, // always import after BrowserModule
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatAutocompleteModule,
    MatTableModule,
    MatSelectModule,
    MatPaginatorModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatTreeModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
