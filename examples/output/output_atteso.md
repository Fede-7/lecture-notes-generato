# 1 Teoria della Stima: Stimatori Non Bayesiani e Test di Ipotesi

*(Basato sulla lezione del 21-05-2026, trascrizione: `input_atteso.txt`)*

---

> **Introduzione**:  
> La **teoria della stima** rappresenta un pilastro fondamentale della **statistica inferenziale**, con applicazioni in ingegneria, scienze dei dati, intelligenza artificiale e comunicazioni. Questo documento tratta **stimatori non bayesiani**, il **limite di Cramér-Rao**, l'**efficienza degli stimatori** e i **test di ipotesi**, con particolare attenzione alla **stima a massima verosimiglianza (MLE)** e ai **test di Neyman-Pearson**. La trattazione è rivolta a studenti universitari di corsi avanzati di probabilità e statistica.

---

## 1.1 Contesto e Motivazioni

### 1.1.1 Stimatori Bayesiani vs. Non Bayesiani

**Stimatore Bayesiano**:  
Approccio in cui il **parametro incognito** $\theta$ è modellato come una **variabile aleatoria** con una **distribuzione a priori** $p(\theta)$. L'obiettivo è calcolare la **distribuzione a posteriori** $p(\theta | x)$ e derivare stime (es. **MMSE**, **MAP**).

> **Osservazione**:  
> Gli stimatori bayesiani sono ottimali quando si dispone di **informazioni a priori** affidabili sul parametro. Tuttavia, in molti contesti applicativi, tali informazioni **non sono disponibili** o **non sono credibili**.

**Stimatore Non Bayesiano**:  
Approccio in cui il **parametro incognito** $\theta$ è trattato come una **costante deterministica** (non aleatoria). Non si assume alcuna distribuzione a priori su $\theta$.

> **Interpretazione**:  
> Un stimatore non bayesiano può essere visto come il **limite di uno stimatore MAP** quando la **densità a priori** $p(\theta)$ è **uniforme** su un insieme finito di valori possibili. In tal caso, la derivata della densità a priori è nulla, e il termine $\ln p(\theta)$ scompare dalla funzione obiettivo del MAP.

---

## 1.2 Famiglie di Distribuzioni e Funzione di Verosimiglianza

### 1.2.1 Definizione di Famiglia Parametrica

**Famiglia di distribuzioni**:  
Insieme di **PDF (Probability Density Function)** o **PMF (Probability Mass Function)** che dipendono da un **parametro incognito** $\theta \in \Theta$:

- **Caso continuo**: $f_{X^n}(x^n | \theta)$
- **Caso discreto**: $P_{X^n}(x^n | \theta)$

> **Osservazione**:  
> Il vettore aleatorio $X^n = (X_1, X_2, \dots, X_n)$ rappresenta **n osservazioni indipendenti e identicamente distribuite (i.i.d.)** da una distribuzione parametrizzata da $\theta$.

### 1.2.2 Funzione di Verosimiglianza

**Funzione di verosimiglianza** $L(\theta | x^n)$:  
Funzione che esprime la **probabilità (o densità) dei dati osservati** $x^n$ **condizionata al parametro** $\theta$:

**Definizione formale**:

```
L(θ | x^n) = f_{X^n}(x^n | θ)  [Caso continuo]
L(θ | x^n) = P_{X^n}(x^n | θ)  [Caso discreto]
```

**Log-verosimiglianza** $\lambda(\theta | x^n)$:  
Logaritmo della funzione di verosimiglianza, spesso più agevole da manipolare analiticamente:

$$  
\lambda(\theta | x^n) = \ln L(\theta | x^n)  
$$

> **Proprietà**:  
> La **massimizzazione della verosimiglianza** è equivalente alla **massimizzazione della log-verosimiglianza**, poiché il logaritmo è una funzione **monotonamente crescente**.

---

## 1.3 Stima a Massima Verosimiglianza (MLE)

### 1.3.1 Definizione

**Stimatore a Massima Verosimiglianza (MLE)**:  
Stimatore che **massimizza la funzione di verosimiglianza** (o log-verosimiglianza) rispetto a $\theta$:

**Definizione formale**:  
`**Stimatore MLE: $\hat{\theta}_{MLE}(x^n) = \arg\max_{\theta \in \Theta} L(\theta | x^n) = \arg\max_{\theta \in \Theta} \lambda(\theta | x^n)$**`

> **Osservazione**:  
> La **stima MLE** è una **realizzazione** dello stimatore $\hat{\theta}_{MLE}(X^n)$, che è una **variabile aleatoria** (dipende dai dati osservati).

### 1.3.2 Proprietà Asintotiche

Lo stimatore MLE gode delle seguenti proprietà **asintotiche** (per $n \to \infty$):


| Proprietà                             | Descrizione                                | Formula                                                                |
| ------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------- |
| **Non polarizzato (asintoticamente)** | $E[\hat{\theta}_{MLE}] \to \theta$         | $\lim_{n\to\infty} E[\hat{\theta}_n] = \theta$                         |
| **Consistente in probabilità**        | $\hat{\theta}_{MLE} \to^P \theta$          | $\lim_{n\to\infty} P(                                                  |
| **Consistente in media quadratica**   | $E[(\hat{\theta}_{MLE} - \theta)^2] \to 0$ | $\lim_{n\to\infty} E[(\hat{\theta}_n - \theta)^2] = 0$                 |
| **Asintoticamente efficiente**        | Raggiunge il **limite di Cramér-Rao**      | $\lim_{n\to\infty} \text{Var}(\hat{\theta}_n) = \frac{1}{I_n(\theta)}$ |


⚠️ **Attenzione**:  
La **consistenza in media quadratica** implica la **consistenza in probabilità** (per la disuguaglianza di Chebyshev), ma **non vale il viceversa**.

---

## 1.4 Proprietà degli Stimatori: Non Polarizzazione e Consistenza

### 1.4.1 Stimatore Non Polarizzato (Unbiased)

**Definizione formale**:  
`**Stimatore non polarizzato: Uno stimatore $\hat{\theta}(X^n)$ è non polarizzato (o unbiased) se il suo valore atteso è uguale al vero parametro $\theta$: $E[\hat{\theta}(X^n)] = \theta$**`

> **Osservazione**:  
> Per uno stimatore non polarizzato, l'**errore quadratico medio (MSE)** coincide con la **varianza** dello stimatore:  
> $$\text{MSE} = E[(\hat{\theta} - \theta)^2] = \text{Var}(\hat{\theta})$$

### 1.4.2 Stimatore Consistente

**Definizione formale**:  
`**Consistenza in media quadratica: Uno stimatore $\hat{\theta}(X^n)$ è consistente in media quadratica se $\lim_{n\to\infty} E[(\hat{\theta}_n - \theta)^2] = 0$**`

`**Consistenza in probabilità: Uno stimatore $\hat{\theta}(X^n)$ è consistente in probabilità se $\lim_{n\to\infty} P(|\hat{\theta}_n - \theta| > \epsilon) = 0$ per ogni $\epsilon > 0$**`

---

## 1.5 Informazione di Fisher e Limite di Cramér-Rao

### 1.5.1 Informazione di Fisher

**Definizione formale**:  
`**Informazione di Fisher: L'informazione di Fisher $I_n(\theta)$ è definita come l'opposto del valore atteso della derivata seconda della log-verosimiglianza rispetto a $\theta$:**`

$$  
I_n(\theta) = -E\left[\frac{d^2}{d\theta^2} \lambda(\theta | X^n)\right] = E\left[\left(\frac{d}{d\theta} \lambda(\theta | X^n)\right)^2\right]  
$$

> **Osservazione**:  
> L'informazione di Fisher misura **quanta informazione** i dati $X^n$ contengono sul parametro $\theta$. Maggiore è $I_n(\theta)$, minore è l'**incertezza** sulla stima di $\theta$.

### 1.5.2 Disuguaglianza di Cramér-Rao

**Teorema (Disuguaglianza di Cramér-Rao)**:  
Per **qualsiasi stimatore non polarizzato** $\hat{\theta}(X^n)$, la varianza è **limitata inferiormente** dall'**inverso dell'informazione di Fisher**:

$$  
\text{Var}(\hat{\theta}(X^n)) \geq \frac{1}{I_n(\theta)}  
$$

> **Implicazione**:  
> Il limite di Cramér-Rao rappresenta il **minimo errore quadratico medio** raggiungibile da **qualsiasi stimatore non polarizzato**. Se uno stimatore raggiunge questo limite, è **ottimo** in termini di MSE.

### 1.5.3 Dimostrazione della Disuguaglianza di Cramér-Rao

**Ipotesi**:

- $X^n$ è un vettore aleatorio **discreto** con PMF $P_{X^n}(x^n | \theta)$ (la dimostrazione per il caso continuo è analoga).
- Lo stimatore $\hat{\theta}(X^n)$ è **non polarizzato**: $E[\hat{\theta}] = \theta$.

**Passo 1: Normalizzazione della PMF**  
$$  
\sum_{x^n} P_{X^n}(x^n | \theta) = 1  
$$  
Derivando rispetto a $\theta$:  
$$  
\sum_{x^n} \frac{d}{d\theta} P_{X^n}(x^n | \theta) = 0  
$$  
Che può essere riscritto come:  
$$  
\sum_{x^n} \frac{d}{d\theta} \ln P_{X^n}(x^n | \theta) \cdot P_{X^n}(x^n | \theta) = 0  
$$  
Quindi:  
$$  
E\left[\frac{d}{d\theta} \lambda(\theta | X^n)\right] = 0  
$$

**Passo 2: Derivazione della relazione chiave**  
Derivando nuovamente rispetto a $\theta$:  
$$  
\sum_{x^n} \left[\frac{d^2}{d\theta^2} \lambda(\theta | x^n) \cdot P_{X^n}(x^n | \theta) + \left(\frac{d}{d\theta} \lambda(\theta | x^n)\right)^2 \cdot P_{X^n}(x^n | \theta)\right] = 0  
$$  
Da cui si ottiene:  
$$  
E\left[\frac{d^2}{d\theta^2} \lambda(\theta | X^n)\right] + E\left[\left(\frac{d}{d\theta} \lambda(\theta | X^n)\right)^2\right] = 0  
$$  
Quindi:  
$$  
E\left[\left(\frac{d}{d\theta} \lambda(\theta | X^n)\right)^2\right] = -E\left[\frac{d^2}{d\theta^2} \lambda(\theta | X^n)\right] = I_n(\theta)  
$$

**Passo 3: Applicazione della non polarizzazione**  
Dalla non polarizzazione:  
$$  
\sum_{x^n} \hat{\theta}(x^n) P_{X^n}(x^n | \theta) = \theta  
$$  
Derivando rispetto a $\theta$:  
$$  
\sum_{x^n} \hat{\theta}(x^n) \frac{d}{d\theta} P_{X^n}(x^n | \theta) = 1  
$$  
Che può essere riscritto come:  
$$  
\sum_{x^n} \hat{\theta}(x^n) \frac{d}{d\theta} \lambda(\theta | x^n) P_{X^n}(x^n | \theta) = 1  
$$  
Quindi:  
$$  
E\left[\hat{\theta}(X^n) \cdot \frac{d}{d\theta} \lambda(\theta | X^n)\right] = 1  
$$

**Passo 4: Covarianza e Disuguaglianza di Cauchy-Schwarz**  
Sia $Z_1 = \hat{\theta}(X^n)$ e $Z_2 = \frac{d}{d\theta} \lambda(\theta | X^n)$. Allora:  
$$  
\text{Cov}(Z_1, Z_2) = E[Z_1 Z_2] - E[Z_1]E[Z_2] = 1 - \theta \cdot 0 = 1  
$$  
Per la **disuguaglianza di Cauchy-Schwarz**:  
$$  
\text{Cov}(Z_1, Z_2)^2 \leq \text{Var}(Z_1) \text{Var}(Z_2)  
$$  
Quindi:  
$$  
1 \leq \text{Var}(\hat{\theta}) \cdot I_n(\theta)  
$$  
Da cui:  
$$  
\text{Var}(\hat{\theta}) \geq \frac{1}{I_n(\theta)}  
$$

---

## 1.6 Efficienza degli Stimatori

### 1.6.1 Stimatore Efficiente

**Definizione formale**:  
`**Stimatore efficiente: Uno stimatore non polarizzato $\hat{\theta}(X^n)$ è efficiente se la sua varianza è uguale al limite di Cramér-Rao:**`

$$  
\text{Var}(\hat{\theta}(X^n)) = \frac{1}{I_n(\theta)}  
$$

> **Osservazione**:  
> Se uno stimatore è efficiente, **nessun altro stimatore non polarizzato** può avere un **errore quadratico medio minore**.

### 1.6.2 Stimatore Asintoticamente Efficiente

**Definizione formale**:  
`**Stimatore asintoticamente efficiente: Uno stimatore $\hat{\theta}(X^n)$ è asintoticamente efficiente se $\lim_{n\to\infty} \text{Var}(\hat{\theta}_n) = \frac{1}{I_n(\theta)}$**`

⚠️ **Attenzione**:

- Se lo **stimatore MLE non raggiunge il limite di Cramér-Rao**, allora **nessun stimatore efficiente esiste** per quel problema.
- Se lo **stimatore MLE raggiunge il limite di Cramér-Rao**, allora è **ottimo** in termini di MSE.

---

## 1.7 Esempi Pratici

### 1.7.1 Esempio 1: Stima del Parametro di una Distribuzione di Laplace

**Problema**:  
Sia $X^n = (X_1, X_2, \dots, X_n)$ un campione i.i.d. da una **distribuzione di Laplace** con parametro $\mu > 0$, dove la PDF è:

$$  
f_{X}(x | \mu) = \frac{1}{2\mu} e^{-|x|/\mu}, \quad x \in \mathbb{R}  
$$

**Obiettivi**:

1. Trovare lo **stimatore MLE** di $\mu$.
2. Dimostrare che è **non polarizzato**.
3. Dimostrare che è **consistente in media quadratica**.
4. Dimostrare che è **efficiente**.

---

#### 1.7.1.1 Stimatore MLE

**Log-verosimiglianza**:  
$$  
\lambda(\mu | x^n) = \ln \left(\prod_{i=1}^n \frac{1}{2\mu} e^{-|x_i|/\mu}\right) = -n \ln(2\mu) - \frac{1}{\mu} \sum_{i=1}^n |x_i|  
$$

**Derivata della log-verosimiglianza**:  
$$  
\frac{d}{d\mu} \lambda(\mu | x^n) = -\frac{n}{\mu} + \frac{1}{\mu^2} \sum_{i=1}^n |x_i|  
$$

**Equazione per il MLE**:  
$$  
-\frac{n}{\hat{\mu}*{MLE}} + \frac{1}{\hat{\mu}*{MLE}^2} \sum_{i=1}^n |x_i| = 0 \implies \hat{\mu}*{MLE} = \frac{1}{n} \sum*{i=1}^n |x_i|  
$$

**Stimatore MLE**:  
$$  
\hat{\mu}*{MLE}(X^n) = \frac{1}{n} \sum*{i=1}^n |X_i|  
$$

---

#### 1.7.1.2 Non Polarizzazione

**Media dello stimatore**:  
$$  
E[\hat{\mu}*{MLE}] = E\left[\frac{1}{n} \sum*{i=1}^n |X_i|\right] = \frac{1}{n} \sum_{i=1}^n E[|X_i|] = E[|X_1|]  
$$

**Calcolo di $E[|X_1|]$**:  
$$  
E[|X_1|] = \int_{-\infty}^{\infty} |x| \cdot \frac{1}{2\mu} e^{-|x|/\mu} dx = 2 \int_{0}^{\infty} x \cdot \frac{1}{2\mu} e^{-x/\mu} dx  
$$  
Ponendo $a = 1/\mu$ e $m = 2$ (integrazione per parti):  
$$  
E[|X_1|] = \frac{1}{\mu} \int_{0}^{\infty} x e^{-x/\mu} dx = \frac{1}{\mu} \cdot \frac{\mu^2}{1^2} \Gamma(2) = \frac{1}{\mu} \cdot \mu^2 \cdot 1! = \mu  
$$  
Quindi:  
$$  
E[\hat{\mu}_{MLE}] = \mu  
$$  
**Conclusione**: Lo stimatore è **non polarizzato**.

---

#### 1.7.1.3 Consistenza in Media Quadratica

**Varianza dello stimatore**:  
$$  
\text{Var}(\hat{\mu}*{MLE}) = \text{Var}\left(\frac{1}{n} \sum*{i=1}^n |X_i|\right) = \frac{1}{n^2} \sum_{i=1}^n \text{Var}(|X_i|) = \frac{1}{n} \text{Var}(|X_1|)  
$$

**Calcolo di $\text{Var}(|X_1|)$**:  
$$  
\text{Var}(|X_1|) = E[|X_1|^2] - (E[|X_1|])^2  
$$

**Calcolo di $E[|X_1|^2]$**:  
$$  
E[X_1^2] = \int_{-\infty}^{\infty} x^2 \cdot \frac{1}{2\mu} e^{-|x|/\mu} dx = 2 \int_{0}^{\infty} x^2 \cdot \frac{1}{2\mu} e^{-x/\mu} dx = \frac{1}{\mu} \cdot \frac{\mu^3}{1^3} \Gamma(3) = \frac{1}{\mu} \cdot \mu^3 \cdot 2! = 2\mu^2  
$$  
Quindi:  
$$  
\text{Var}(|X_1|) = 2\mu^2 - \mu^2 = \mu^2  
$$

**Varianza dello stimatore**:  
$$  
\text{Var}(\hat{\mu}_{MLE}) = \frac{\mu^2}{n}  
$$

**Limite per $n \to \infty$**:  
$$  
\lim_{n\to\infty} \text{Var}(\hat{\mu}_{MLE}) = 0  
$$  
**Conclusione**: Lo stimatore è **consistente in media quadratica** (e quindi anche in probabilità).

---

#### 1.7.1.4 Efficienza

**Calcolo dell'informazione di Fisher**:  
Dalla log-verosimiglianza:  
$$  
\lambda(\mu | x^n) = -n \ln(2\mu) - \frac{1}{\mu} \sum_{i=1}^n |x_i|  
$$

**Derivata prima**:  
$$  
\frac{d}{d\mu} \lambda(\mu | x^n) = -\frac{n}{\mu} + \frac{1}{\mu^2} \sum_{i=1}^n |x_i|  
$$

**Derivata seconda**:  
$$  
\frac{d^2}{d\mu^2} \lambda(\mu | x^n) = \frac{n}{\mu^2} - \frac{2}{\mu^3} \sum_{i=1}^n |x_i|  
$$

**Valore atteso della derivata seconda**:  
$$  
E\left[\frac{d^2}{d\mu^2} \lambda(\mu | X^n)\right] = \frac{n}{\mu^2} - \frac{2}{\mu^3} \sum_{i=1}^n E[|X_i|] = \frac{n}{\mu^2} - \frac{2}{\mu^3} \cdot n \mu = \frac{n}{\mu^2} - \frac{2n}{\mu^2} = -\frac{n}{\mu^2}  
$$

**Informazione di Fisher**:  
$$  
I_n(\mu) = -E\left[\frac{d^2}{d\mu^2} \lambda(\mu | X^n)\right] = \frac{n}{\mu^2}  
$$

**Limite di Cramér-Rao**:  
$$  
\frac{1}{I_n(\mu)} = \frac{\mu^2}{n}  
$$

**Confronti con la varianza dello stimatore**:  
$$  
\text{Var}(\hat{\mu}_{MLE}) = \frac{\mu^2}{n} = \frac{1}{I_n(\mu)}  
$$  
**Conclusione**: Lo stimatore è **efficiente**.

---

### 1.7.2 Esempio 2: Test di Ipotesi con Due Sorgenti Binarie

**Problema**:  
Si abbiano due sorgenti binarie senza memoria:

- **Sorgente $S_1$**: Emette `1` con probabilità $p_1$.
- **Sorgente $S_2$**: Emette `1` con probabilità $p_2 < p_1$.

La sorgente $S_1$ è attiva con probabilità $\pi_1$, mentre $S_2$ è attiva con probabilità $\pi_2 = 2\pi_1$ (quindi $\pi_1 = 1/3$, $\pi_2 = 2/3$).  
L'osservabile è $Y$, il numero di `1` in una stringa di lunghezza $n = 100$.

**Obiettivi**:

1. Determinare la **regola a minima probabilità di errore** (MAP) per decidere quale sorgente è attiva.
2. Calcolare la **probabilità di errore** corrispondente.
3. Determinare il **test di Neyman-Pearson** per discriminare tra $H_0: S_2$ attiva e $H_1: S_1$ attiva.

---

#### 1.7.2.1 Regola MAP

**Ipotesi**:

- $H_1$: $S_1$ è attiva ($Y \sim \text{Binomiale}(n, p_1)$).
- $H_2$: $S_2$ è attiva ($Y \sim \text{Binomiale}(n, p_2)$).

**Regola MAP**:  
Scegli $H_1$ se:  
$$  
P(Y = y | H_1) \pi_1 > P(Y = y | H_2) \pi_2  
$$  
Sostituendo $\pi_2 = 2\pi_1$:  
$$  
P(Y = y | H_1) > 2 P(Y = y | H_2)  
$$

**PMF Binomiale**:  
$$  
P(Y = y | H_i) = \binom{n}{y} p_i^y (1 - p_i)^{n - y}, \quad i = 1, 2  
$$

**Rapporto di verosimiglianza**:  
$$  
\frac{P(Y = y | H_1)}{P(Y = y | H_2)} = \left(\frac{p_1}{p_2}\right)^y \left(\frac{1 - p_2}{1 - p_1}\right)^{n - y} \cdot \frac{p_1^{n - y} (1 - p_1)^{n - y}}{p_2^{n - y} (1 - p_2)^{n - y}} = \left(\frac{p_1}{p_2}\right)^y \left(\frac{1 - p_2}{1 - p_1}\right)^{n - y} \cdot \left(\frac{p_1}{p_2}\right)^{n - y} \left(\frac{1 - p_2}{1 - p_1}\right)^y  
$$  
Semplificando:  
$$  
\frac{P(Y = y | H_1)}{P(Y = y | H_2)} = \left(\frac{p_1 (1 - p_2)}{p_2 (1 - p_1)}\right)^y \left(\frac{p_1}{p_2}\right)^{n - y} \left(\frac{1 - p_2}{1 - p_1}\right)^y  
$$

**Regola semplificata**:  
Scegli $H_1$ se:  
$$  
\left(\frac{p_1}{p_2}\right)^y \left(\frac{1 - p_2}{1 - p_1}\right)^{n - y} > 2  
$$  
Prendendo il logaritmo:  
$$  
y \ln\left(\frac{p_1}{p_2}\right) + (n - y) \ln\left(\frac{1 - p_2}{1 - p_1}\right) > \ln(2)  
$$

**Soglia**:  
$$  
y > \frac{\ln(2) - n \ln\left(\frac{1 - p_2}{1 - p_1}\right)}{\ln\left(\frac{p_1}{p_2}\right) - \ln\left(\frac{1 - p_2}{1 - p_1}\right)} = \eta  
$$

---

#### 1.7.2.2 Probabilità di Errore

**Probabilità di errore totale**:  
$$  
P(\text{errore}) = P(\text{errore} | H_1) \pi_1 + P(\text{errore} | H_2) \pi_2  
$$

**Errore sotto $H_1$**:  
Decido $H_2$ se $Y < \eta$:  
$$  
P(\text{errore} | H_1) = P(Y < \eta | H_1) = \sum_{y=0}^{\lfloor \eta \rfloor} \binom{n}{y} p_1^y (1 - p_1)^{n - y}  
$$

**Errore sotto $H_2$**:  
Decido $H_1$ se $Y \geq \eta$:  
$$  
P(\text{errore} | H_2) = P(Y \geq \eta | H_2) = \sum_{y=\lceil \eta \rceil}^n \binom{n}{y} p_2^y (1 - p_2)^{n - y}  
$$

**Probabilità di errore**:  
$$  
P(\text{errore}) = \frac{1}{3} \sum_{y=0}^{\lfloor \eta \rfloor} \binom{n}{y} p_1^y (1 - p_1)^{n - y} + \frac{2}{3} \sum_{y=\lceil \eta \rceil}^n \binom{n}{y} p_2^y (1 - p_2)^{n - y}  
$$

---

#### 1.7.2.3 Test di Neyman-Pearson

**Ipotesi**:

- $H_0$: $S_2$ è attiva ($Y \sim \text{Binomiale}(n, p_2)$).
- $H_1$: $S_1$ è attiva ($Y \sim \text{Binomiale}(n, p_1)$).

**Test di Neyman-Pearson**:  
Scegli $H_1$ se:  
$$  
\Lambda(Y) = \frac{P(Y | H_1)}{P(Y | H_2)} > \lambda  
$$  
Dove $\lambda$ è scelto in modo che la **probabilità di falso allarme (PFA)** sia uguale a $\alpha$:  
$$  
P(\text{decido } H_1 | H_0) = \alpha  
$$

**Rapporto di verosimiglianza**:  
$$  
\Lambda(Y) = \left(\frac{p_1}{p_2}\right)^Y \left(\frac{1 - p_1}{1 - p_2}\right)^{n - Y}  
$$

**Test**:  
Scegli $H_1$ se:  
$$  
Y \ln\left(\frac{p_1}{p_2}\right) + (n - Y) \ln\left(\frac{1 - p_1}{1 - p_2}\right) > \ln(\lambda)  
$$

**Soglia**:  
$$  
Y > \frac{\ln(\lambda) - n \ln\left(\frac{1 - p_1}{1 - p_2}\right)}{\ln\left(\frac{p_1}{p_2}\right) - \ln\left(\frac{1 - p_1}{1 - p_2}\right)} = \eta'  
$$

**PFA**:  
$$  
\alpha = P(Y \geq \eta' | H_0) = \sum_{y=\lceil \eta' \rceil}^n \binom{n}{y} p_2^y (1 - p_2)^{n - y}  
$$

⚠️ **Attenzione**:  
Non sempre esiste un $\eta'$ intero che soddisfi esattamente $\alpha$. In tal caso, si ricorre alla **randomizzazione** della soglia.

---

### 1.7.3 Esempio 3: Test di Neyman-Pearson per Distribuzione Esponenziale

**Problema**:  
Sia $X$ un osservabile con:

- $H_0$: $X \sim \text{Exp}(\mu_0)$ (PDF: $f_{X|H_0}(x) = \frac{1}{\mu_0} e^{-x/\mu_0}$).
- $H_1$: $X \sim \text{Exp}(\mu_1)$ con $\mu_1 > \mu_0$ (PDF: $f_{X|H_1}(x) = \frac{1}{\mu_1} e^{-x/\mu_1}$).

**Obiettivi**:

1. Determinare il **test di Neyman-Pearson**.
2. Determinare la **soglia** $\eta$ in funzione di $\alpha$ (PFA).
3. Determinare la **curva ROC** (relazione tra $1 - \beta$ e $\alpha$).

---

#### 1.7.3.1 Test di Neyman-Pearson

**Rapporto di verosimiglianza**:  
$$  
\Lambda(X) = \frac{f_{X|H_1}(x)}{f_{X|H_0}(x)} = \frac{\frac{1}{\mu_1} e^{-x/\mu_1}}{\frac{1}{\mu_0} e^{-x/\mu_0}} = \frac{\mu_0}{\mu_1} e^{-x (1/\mu_1 - 1/\mu_0)}  
$$

**Test**:  
Scegli $H_1$ se:  
$$  
\frac{\mu_0}{\mu_1} e^{-x (1/\mu_1 - 1/\mu_0)} > \lambda \iff e^{x (1/\mu_0 - 1/\mu_1)} > \lambda \frac{\mu_1}{\mu_0}  
$$  
Prendendo il logaritmo:  
$$  
x > \frac{\ln(\lambda) + \ln(\mu_1 / \mu_0)}{1/\mu_0 - 1/\mu_1} = \eta  
$$

---

#### 1.7.3.2 Soglia e PFA

**PFA**:  
$$  
\alpha = P(\text{decido } H_1 | H_0) = P(X > \eta | H_0) = e^{-\eta / \mu_0}  
$$

**Soglia**:  
$$  
\eta = -\mu_0 \ln(\alpha)  
$$

---

#### 1.7.3.3 Potenza del Test e Curva ROC

**Potenza del test** ($1 - \beta$):  
Probabilità di **rilevare correttamente** $H_1$:  
$$  
1 - \beta = P(\text{decido } H_1 | H_1) = P(X > \eta | H_1) = e^{-\eta / \mu_1}  
$$

Sostituendo $\eta = -\mu_0 \ln(\alpha)$:  
$$  
1 - \beta = e^{-(-\mu_0 \ln(\alpha)) / \mu_1} = e^{(\mu_0 / \mu_1) \ln(\alpha)} = \alpha^{\mu_0 / \mu_1}  
$$

**Curva ROC**:  
$$  
1 - \beta = \alpha^{\mu_0 / \mu_1}  
$$

> **Applicazione alle comunicazioni ottiche**:  
> In un sistema **on-off keying (OOK)**, $X$ rappresenta l'**energia misurata** in un intervallo di segnalazione:
>
> - $H_0$: **Nessun impulso** (solo rumore, $X \sim \text{Exp}(\mu_0)$).
> - $H_1$: **Impulso presente** (segnale + rumore, $X \sim \text{Exp}(\mu_1)$).
>
> Il rapporto $\mu_1 / \mu_0 = 1 + \text{SNR}$ (dove **SNR** è il *Signal-to-Noise Ratio*).
>
> **Interpretazione**:
>
> - Se **SNR → ∞**, allora $1 - \beta \to 1$ (rilevazione perfetta).
> - Se **SNR → 0**, allora $1 - \beta \to \alpha$ (nessun miglioramento rispetto al caso random).

---

## 1.8 Riassunto delle Proprietà Chiave


| Concetto                                 | Definizione                                                 | Formula                 | Proprietà                                      |
| ---------------------------------------- | ----------------------------------------------------------- | ----------------------- | ---------------------------------------------- |
| **Stimatore non polarizzato**            | $E[\hat{\theta}] = \theta$                                  | -                       | Minimizza il bias                              |
| **Stimatore consistente in MSE**         | $\lim_{n\to\infty} E[(\hat{\theta}_n - \theta)^2] = 0$      | -                       | Garantisce convergenza in media quadratica     |
| **Stimatore consistente in probabilità** | $\lim_{n\to\infty} P(                                       | \hat{\theta}_n - \theta | > \epsilon) = 0$                               |
| **Informazione di Fisher**               | $I_n(\theta) = -E\left[\frac{d^2}{d\theta^2} \lambda(\theta | X^n)\right]$            | -                                              |
| **Limite di Cramér-Rao**                 | $\text{Var}(\hat{\theta}) \geq 1 / I_n(\theta)$             | -                       | Limite inferiore per stimatori non polarizzati |
| **Stimatore efficiente**                 | $\text{Var}(\hat{\theta}) = 1 / I_n(\theta)$                | -                       | Raggiunge il limite di Cramér-Rao              |
| **Stimatore MLE**                        | $\hat{\theta}*{MLE} = \arg\max*{\theta} L(\theta            | x^n)$                   | -                                              |


---

## 1.9 Esercizi Proposti

### 1.9.1 Esercizio 1: Distribuzione Normale

Sia $X^n$ un campione i.i.d. da una distribuzione normale $\mathcal{N}(\mu, \sigma^2)$ con $\sigma^2$ noto.

1. Trova lo **stimatore MLE** di $\mu$.
2. Dimostra che è **non polarizzato** e **efficiente**.
3. Calcola la **varianza asintotica** dello stimatore.

### 1.9.2 Esercizio 2: Distribuzione di Poisson

Sia $X^n$ un campione i.i.d. da una distribuzione di Poisson con parametro $\lambda$.

1. Trova lo **stimatore MLE** di $\lambda$.
2. Dimostra che è **non polarizzato** e **consistente in media quadratica**.
3. Calcola l'**informazione di Fisher** e verifica se lo stimatore è **efficiente**.

### 1.9.3 Esercizio 3: Test di Ipotesi per Bernoulli

Sia $X \sim \text{Bernoulli}(p)$. Si vuole testare:

- $H_0: p = 0.5$ vs. $H_1: p = 0.7$.

1. Determina il **test di Neyman-Pearson** con $\alpha = 0.05$.
2. Calcola la **potenza del test** ($1 - \beta$).

### 1.9.4 Esercizio 4: Distribuzione Esponenziale (Due Parametri)

Sia $X^n$ un campione i.i.d. da una distribuzione esponenziale $\text{Exp}(\lambda)$.

1. Trova lo **stimatore MLE** di $\lambda$.
2. Dimostra che è **non polarizzato** e **efficiente**.
3. Calcola la **varianza asintotica** dello stimatore.

---

## 1.10 Riferimenti e Approfondimenti

- **Libri consigliati**:
  - *"Statistical Inference"* di Casella e Berger (per una trattazione rigorosa della teoria della stima).
  - *"Introduction to the Theory of Statistics"* di Mood, Graybill e Boes (per esempi pratici).
  - *"Detection, Estimation, and Modulation Theory"* di Van Trees (per applicazioni in comunicazioni).
- **Risorse online**:
  - [Wikipedia: Maximum Likelihood Estimation](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation)
  - [Wikipedia: Cramér-Rao Bound](https://en.wikipedia.org/wiki/Cram%C3%A9r%E2%80%93Rao_bound)
  - [Wikipedia: Neyman-Pearson Lemma](https://en.wikipedia.org/wiki/Neyman%E2%80%93Pearson_lemma)

---

> **Nota finale**:  
> Questo documento è stato generato a partire dalla trascrizione di una lezione universitaria. Per un apprendimento ottimale, si consiglia di **affiancare la lettura con esercizi pratici** e di consultare i **testi di riferimento** per approfondimenti teorici. In caso di dubbi, rivolgiti al docente o ai tutor del corso.