import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DirectoryComponent } from './directory/directory.component';

const appRoutes: Routes = [
    { 
        path: 'directory',
        component: DirectoryComponent,
    },
    { 
        path: '', 
        redirectTo: '/directory',
        pathMatch: 'full' 
    },
];

@NgModule({
    imports: [
        RouterModule.forRoot(
            appRoutes,
            { enableTracing: true } // <-- debugging purposes only
        )
    ],
    exports: [
        RouterModule
    ]
})
export class AppRoutingModule { }