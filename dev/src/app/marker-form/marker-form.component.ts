import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialogModule } from '@angular/material/dialog';
import { Rarity } from '../map/enums/rarity.enum';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MapService } from '../shared/services/map.service';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { finalize, Subscription, tap } from 'rxjs';
import { SelectModule } from 'primeng/select';
import { MarkersApiService } from '../shared/services/markers-api.service';
import { RessourcesService } from '../shared/services/ressources.service';
import { RESOURCE_CATEGORIES, TIMERS_BY_CATEGORIES } from '../map/enums/ressources';

export interface MarkerForm {
  type: string, 
  rarity: string, 
  timer: number  
}

@Component({
  selector: 'app-marker-form',
  templateUrl: './marker-form.component.html',
  styleUrls: ['./marker-form.component.scss'],
  imports: [
    MatDialogModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatButtonModule,
    MatInputModule,
    MatIconModule,
    MatSlideToggleModule,
    SelectModule
  ],
})
export class MarkerFormComponent implements OnInit, OnDestroy {
  #mapService = inject(MapService);
  #markerApiService = inject(MarkersApiService);
  #resourcesService = inject(RessourcesService);
  ressourceImages = this.#resourcesService.getAllResources(); 
  rarities = Object.keys(Rarity); // Raretés

  updateTimerSubscribe: Subscription | null | undefined = null; 
  updateRessourceSubscribe: Subscription | null | undefined = null; 

  // FormGroup pour regrouper les 3 FormControl
  markerForm = new FormGroup({
    label: new FormControl(''),
    coord: new FormControl(''),
    type: new FormControl('', Validators.required),
    rarity: new FormControl('', Validators.required), 
    timer: new FormControl({ value: 1, disabled: true }),
    updateTimer: new FormControl(false),
  });

  initialFormData: any;

  // Références injectées
  dialogRef = inject(MatDialogRef<MarkerFormComponent>);
  data: any = inject(MAT_DIALOG_DATA);

  ngOnInit(): void {
    // Si des données existent, mettre à jour le formulaire
    const customMarkerInfo = this.data?.customData;
    if (this.data) {
      const rarity = customMarkerInfo?.rarity ? customMarkerInfo.rarity.charAt(0) + customMarkerInfo.rarity.slice(1) : '';
      const alarmAfter = (customMarkerInfo.alarmAfter - customMarkerInfo.startTime) / 3600;
      this.markerForm.patchValue({
        label: customMarkerInfo.label,
        coord: customMarkerInfo.inGameCoord,
        type: customMarkerInfo.type,
        rarity: rarity,
        timer: alarmAfter,
        updateTimer: false
      });
    } else {
      this.markerForm.get('timer')?.enable();
    }

    this.updateTimerSubscribe = this.markerForm.get('updateTimer')?.valueChanges.subscribe((isEnabled) => {
      const timerControl = this.markerForm.get('timer');
      if (isEnabled) {
        timerControl?.enable(); // Enable the timer field
      } else {
        timerControl?.disable(); // Disable the timer field
      }
    });

    // Auto update timer depending on selected resource 
    this.updateRessourceSubscribe = this.markerForm.get('type')?.valueChanges.subscribe((resourceName) => {
      if (resourceName) {
        const category = this.#resourcesService.getResourceCategory(resourceName)
        const categoryTimer = TIMERS_BY_CATEGORIES[category || 1]; 
        this.markerForm.get('timer')?.setValue(categoryTimer);
      }
    });

    this.initialFormData = this.markerForm.value;
  }

  // Soumettre les données et fermer la popup
  submitForm(): void {
    if (this.markerForm.valid) {
      this.dialogRef.close(this.markerForm.value); // Ferme le dialogue et retourne les valeurs du formulaire
    }
  }

  removeMarker(): void {
    if(confirm("T'es sur de vouloir faire cette connerie ??? !!!")) {
      // Enlever le marker de la map      
      this.#markerApiService.deleteMarker(this.data.customData.id).pipe(
        tap(() => {
          this.#mapService.removeMarkerLocaly(this.data);
          this.dialogRef.close();
        }),
        finalize(() => this.dialogRef.close())
      ).subscribe();
      
    }    
  }

  hasFormChanged(): boolean {
    return JSON.stringify(this.markerForm.value) !== JSON.stringify(this.initialFormData);
  }

  // Annuler et fermer la popup
  cancelForm(): void {
    this.dialogRef.close(null);
  }

  ngOnDestroy(): void {
    this.updateTimerSubscribe?.unsubscribe();
    this.updateRessourceSubscribe?.unsubscribe();
  }
}