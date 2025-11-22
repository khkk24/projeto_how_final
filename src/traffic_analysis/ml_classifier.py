import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle
from pathlib import Path


class AccidentSeverityClassifier:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.label_encoders = {}
        self.target_encoder = None
        self.scaler = StandardScaler()
        self.model = None
        self.features_categoricas = [
            'uf', 'tipo_acidente', 'causa_acidente', 'tipo_pista',
            'tracado_via', 'condicao_metereologica', 'fase_dia',
            'sentido_via', 'dia_semana_nome', 'periodo_dia'
        ]
        self.features_numericas = [
            'hora', 'mes', 'ano', 'dia_semana_num',
            'km', 'veiculos', 'pessoas', 'eh_fim_semana', 'eh_noite'
        ]
        self.target = 'classificacao_acidente'
        
    def create_features(self, df):
        df = df.copy()
        df['eh_fim_semana'] = df['dia_semana_num'].isin([5, 6]).astype(int)
        df['eh_noite'] = ((df['hora'] >= 18) | (df['hora'] < 6)).astype(int)
        df['periodo_dia'] = pd.cut(
            df['hora'], 
            bins=[0, 6, 12, 18, 24], 
            labels=['Madrugada', 'Manhã', 'Tarde', 'Noite'],
            include_lowest=True
        )
        return df
    
    def encode_features(self, df, fit=True):
        df_encoded = df.copy()
        
        for col in self.features_categoricas:
            if col in df_encoded.columns:
                if fit:
                    le = LabelEncoder()
                    df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    if col in self.label_encoders:
                        le = self.label_encoders[col]
                        df_encoded[col] = df_encoded[col].astype(str).map(
                            lambda x: le.transform([x])[0] if x in le.classes_ else -1
                        )
        
        if self.target in df_encoded.columns:
            if fit:
                self.target_encoder = LabelEncoder()
                df_encoded['target_encoded'] = self.target_encoder.fit_transform(
                    df_encoded[self.target].astype(str)
                )
            else:
                if self.target_encoder:
                    df_encoded['target_encoded'] = df_encoded[self.target].astype(str).map(
                        lambda x: self.target_encoder.transform([x])[0] if x in self.target_encoder.classes_ else -1
                    )
        
        return df_encoded
    
    def prepare_data(self, df, fit=True):
        df = self.create_features(df)
        df_encoded = self.encode_features(df, fit=fit)
        
        all_features = self.features_categoricas + self.features_numericas
        X = df_encoded[all_features].copy()
        y = df_encoded['target_encoded'] if 'target_encoded' in df_encoded.columns else None
        
        for col in self.features_numericas:
            if col in X.columns:
                if X[col].dtype == 'object':
                    X[col] = X[col].astype(str).str.replace(',', '.').astype(float)
                X[col] = pd.to_numeric(X[col], errors='coerce')
        
        mask = X.notna().all(axis=1)
        if y is not None:
            mask = mask & y.notna()
            y = y[mask]
        
        X = X[mask]
        
        if fit:
            X[self.features_numericas] = self.scaler.fit_transform(X[self.features_numericas])
        else:
            X[self.features_numericas] = self.scaler.transform(X[self.features_numericas])
        
        return X, y if y is not None else None
    
    def train(self, df, model_type='random_forest', test_size=0.2, **model_params):
        df_filtered = df[df[self.target].notna()].copy()
        
        X, y = self.prepare_data(df_filtered, fit=True)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        if model_type == 'random_forest':
            default_params = {
                'n_estimators': 100,
                'max_depth': 20,
                'min_samples_split': 10,
                'random_state': self.random_state,
                'n_jobs': -1
            }
            default_params.update(model_params)
            self.model = RandomForestClassifier(**default_params)
        elif model_type == 'gradient_boosting':
            default_params = {
                'n_estimators': 100,
                'max_depth': 10,
                'learning_rate': 0.1,
                'random_state': self.random_state
            }
            default_params.update(model_params)
            self.model = GradientBoostingClassifier(**default_params)
        else:
            raise ValueError(f"Model type '{model_type}' not supported")
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        
        results = {
            'accuracy': accuracy_score(y_test, y_pred),
            'classification_report': classification_report(
                y_test, y_pred, 
                target_names=self.target_encoder.classes_,
                output_dict=True
            ),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'X_test': X_test,
            'y_test': y_test,
            'y_pred': y_pred,
            'feature_names': self.features_categoricas + self.features_numericas
        }
        
        if hasattr(self.model, 'feature_importances_'):
            results['feature_importance'] = pd.DataFrame({
                'feature': results['feature_names'],
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        
        return results
    
    def predict(self, df):
        X, _ = self.prepare_data(df, fit=False)
        predictions = self.model.predict(X)
        predictions_labels = self.target_encoder.inverse_transform(predictions)
        
        probabilities = None
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(X)
        
        return predictions_labels, probabilities
    
    def save_model(self, path):
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        with open(path / 'model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(path / 'label_encoders.pkl', 'wb') as f:
            pickle.dump(self.label_encoders, f)
        
        with open(path / 'target_encoder.pkl', 'wb') as f:
            pickle.dump(self.target_encoder, f)
        
        with open(path / 'scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        
        metadata = {
            'features_categoricas': self.features_categoricas,
            'features_numericas': self.features_numericas,
            'target': self.target,
            'random_state': self.random_state
        }
        
        with open(path / 'metadata.pkl', 'wb') as f:
            pickle.dump(metadata, f)
    
    def load_model(self, path):
        path = Path(path)
        
        with open(path / 'model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        
        with open(path / 'label_encoders.pkl', 'rb') as f:
            self.label_encoders = pickle.load(f)
        
        with open(path / 'target_encoder.pkl', 'rb') as f:
            self.target_encoder = pickle.load(f)
        
        with open(path / 'scaler.pkl', 'rb') as f:
            self.scaler = pickle.load(f)
        
        with open(path / 'metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
            self.features_categoricas = metadata['features_categoricas']
            self.features_numericas = metadata['features_numericas']
            self.target = metadata['target']
            self.random_state = metadata['random_state']
